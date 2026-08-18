from __future__ import annotations

from functools import reduce
import operator

from cre_rulekit.config import NamespaceConfig
from cre_rulekit.dates import parse_relative_current_date
from cre_rulekit.model import Predicate, RulePlan, RuleReference


def _col_name(namespace: str, field: str) -> str:
    return f"{namespace}__{field}"


class PySparkDataFrameCompiler:
    """
    Compiles RulePlan into a PySpark DataFrame execution plan.

    This backend expects raw_frames as:

        {namespace: spark_dataframe}

    It returns a DataFrame containing rows that pass the rule.
    For empty/true rules, pass universe_df to return all candidate mids;
    otherwise it returns spark.range(1), which is enough for one-mid pass/fail.
    """

    def __init__(self, namespace_config, rule_resolver=None, spark=None):
        self.namespace_config = NamespaceConfig(namespace_config)
        self.rule_resolver = rule_resolver
        self.spark = spark

    def compile(self, plan: RulePlan, raw_frames: dict, mid_value=None, universe_df=None, seen_rules=None):
        from pyspark.sql import functions as F

        seen_rules = seen_rules or set()

        if plan.is_always_true:
            if universe_df is not None:
                return universe_df
            if self.spark is None:
                any_df = next(iter(raw_frames.values()), None)
                if any_df is None:
                    raise ValueError("spark or raw_frames is required for true plan")
                spark = any_df.sparkSession
            else:
                spark = self.spark
            return spark.range(1).select(F.current_date().alias("rule_date"))

        namespaces = plan.namespaces()
        if not namespaces:
            return self._compile_reference_only_plan(plan, raw_frames, mid_value, universe_df, seen_rules)

        prepared = self._prepare_frames(plan, raw_frames, namespaces)
        joined = self._join_frames(prepared, namespaces)

        if mid_value is not None:
            base_ns = namespaces[0]
            mid_col = self.namespace_config.mid_column(base_ns)
            if mid_col:
                joined = joined.filter(F.col(_col_name(base_ns, mid_col)) == F.lit(mid_value))

        predicate = self._compile_plan_predicate(plan, joined, seen_rules)
        if predicate is None:
            return joined
        return joined.filter(predicate)

    def _compile_reference_only_plan(self, plan, raw_frames, mid_value, universe_df, seen_rules):
        if universe_df is None:
            raise ValueError("rulemetadata-only plans require universe_df in PySpark backend")
        predicate_df = universe_df
        # Simple implementation: apply references as semi/anti joins when they are top-level AND groups.
        for group in plan.eval_groups:
            for term in group.terms:
                if not isinstance(term, RuleReference):
                    continue
                nested_df = self._compile_rule_reference_df(term, raw_frames, mid_value, seen_rules)
                predicate_df = self._apply_rule_reference_join(predicate_df, nested_df, term.expected_result)
        return predicate_df

    def _prepare_frames(self, plan, raw_frames, namespaces):
        from pyspark.sql import functions as F

        required = {ns: set() for ns in namespaces}
        for group in plan.eval_groups:
            for term in group.terms:
                if isinstance(term, Predicate):
                    required[term.namespace].add(term.field)

        prepared = {}
        for ns in namespaces:
            cfg = self.namespace_config.get(ns)
            cols = set(required[ns])
            cols.update(cfg.primary_keys)
            if cfg.mid_column:
                cols.add(cfg.mid_column)
            prepared[ns] = raw_frames[ns].select(*[F.col(c).alias(_col_name(ns, c)) for c in cols])
        return prepared

    def _join_frames(self, frames, namespaces):
        from pyspark.sql import functions as F

        base = namespaces[0]
        joined = frames[base]
        base_keys = self.namespace_config.primary_keys(base)
        for ns in namespaces[1:]:
            right_keys = self.namespace_config.primary_keys(ns)
            conds = [
                F.col(_col_name(base, bk)) == F.col(_col_name(ns, rk))
                for bk, rk in zip(base_keys, right_keys)
            ]
            joined = joined.join(frames[ns], reduce(operator.and_, conds), "inner")
        return joined

    def _compile_plan_predicate(self, plan, df, seen_rules):
        group_conditions = []
        for group in plan.eval_groups:
            cond = self._compile_group(group, df, seen_rules)
            if cond is not None:
                group_conditions.append(cond)
        if not group_conditions:
            return None
        return self._combine(group_conditions, plan.op)

    def _compile_group(self, group, df, seen_rules):
        not_equal_terms = [t for t in group.terms if isinstance(t, Predicate) and t.operator == "!="]
        conditions = []

        if len(not_equal_terms) >= 2:
            positive = [self._compile_predicate(t, force_equal=True) for t in not_equal_terms]
            not_block = ~self._combine(positive, "AND")
            inserted = False
            for term in group.terms:
                if isinstance(term, Predicate) and term.operator == "!=":
                    if not inserted:
                        conditions.append(not_block)
                        inserted = True
                else:
                    c = self._compile_term(term, df, seen_rules)
                    if c is not None:
                        conditions.append(c)
        else:
            for term in group.terms:
                c = self._compile_term(term, df, seen_rules)
                if c is not None:
                    conditions.append(c)

        return self._combine(conditions, group.op) if conditions else None

    def _compile_term(self, term, df, seen_rules):
        if isinstance(term, Predicate):
            return self._compile_predicate(term)
        if isinstance(term, RuleReference):
            # For mixed plans, rule references are better applied as semi/anti joins in a separate physical plan.
            raise NotImplementedError("Mixed predicate + rulemetadata PySpark plans need join-phase compilation")
        raise ValueError(f"Unknown term: {term}")

    def _compile_predicate(self, pred: Predicate, force_equal=False):
        from pyspark.sql import functions as F

        c = F.col(_col_name(pred.namespace, pred.field))
        op = "=" if force_equal else pred.operator
        v = self._spark_value(pred.value)

        if op == "=":
            return c.isNull() if pred.value is None else c == v
        if op == "!=":
            return c.isNotNull() if pred.value is None else c != v
        if op == ">":
            return c > v
        if op == ">=":
            return c >= v
        if op == "<":
            return c < v
        if op == "<=":
            return c <= v
        if op == "contains":
            return c.contains(str(pred.value))
        if op in ("in", "has_any"):
            values = pred.value if isinstance(pred.value, list) else [pred.value]
            return c.isin(values)
        if op == "has_all":
            values = pred.value if isinstance(pred.value, list) else [pred.value]
            return reduce(operator.and_, [F.array_contains(c, item) for item in values])
        if op in ("not_in", "has_none"):
            values = pred.value if isinstance(pred.value, list) else [pred.value]
            return ~c.isin(values)
        if op in ("exists", "is_not_null"):
            return c.isNotNull()
        if op in ("not_exists", "is_null"):
            return c.isNull()
        raise ValueError(f"Unsupported operator: {op}")

    def _spark_value(self, value):
        from pyspark.sql import functions as F

        parsed = parse_relative_current_date(value)
        if parsed:
            direction, amount, unit = parsed
            sign = -1 if direction == "ago" else 1
            if unit == "day":
                return F.date_sub(F.current_date(), amount) if sign < 0 else F.date_add(F.current_date(), amount)
            if unit == "week":
                days = amount * 7
                return F.date_sub(F.current_date(), days) if sign < 0 else F.date_add(F.current_date(), days)
            if unit == "month":
                return F.add_months(F.current_date(), sign * amount)
            if unit == "year":
                return F.add_months(F.current_date(), sign * amount * 12)
        return F.lit(value)

    def _combine(self, conditions, op):
        if not conditions:
            return None
        fn = operator.and_ if op == "AND" else operator.or_
        return reduce(fn, conditions)

    def _compile_rule_reference_df(self, ref, raw_frames, mid_value, seen_rules):
        if not self.rule_resolver:
            raise ValueError("rule_resolver is required for rule references")
        if ref.rule_name in seen_rules:
            raise ValueError(f"Circular rule reference found: {ref.rule_name}")
        nested_plan = self.rule_resolver.resolve_plan(ref.rule_name)
        return self.compile(nested_plan, raw_frames, mid_value=mid_value, seen_rules=seen_rules | {ref.rule_name})

    def _apply_rule_reference_join(self, parent_df, nested_df, expected_result):
        # Assumes both frames expose a column named mid or compatible caller-provided universe.
        join_type = "left_semi" if expected_result else "left_anti"
        return parent_df.join(nested_df, "mid", join_type)

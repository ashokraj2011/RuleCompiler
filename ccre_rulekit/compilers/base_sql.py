from __future__ import annotations

import re
from functools import reduce
from textwrap import indent

from ccre_rulekit.config import NamespaceConfig
from ccre_rulekit.dates import parse_relative_current_date
from ccre_rulekit.model import Predicate, RulePlan, RuleReference


_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class BaseSqlCompiler:
    dialect = "base"
    true_sql = "SELECT 1"

    def __init__(self, namespace_config, rule_resolver=None, include_database: bool = False):
        self.namespace_config = NamespaceConfig(namespace_config)
        self.rule_resolver = rule_resolver
        self.include_database = include_database

    def compile(self, plan: RulePlan, mid_value=None, select_clause="*", mid_expression=None, seen_rules=None):
        seen_rules = seen_rules or set()

        if plan.is_always_true:
            return self.true_sql, []

        namespaces = plan.namespaces()
        params = []

        if not namespaces:
            where_sql = self._compile_plan_where(plan, aliases={}, params=params, mid_value=mid_value, mid_expression=mid_expression, seen_rules=seen_rules)
            if not where_sql:
                return self.true_sql, []
            select_value = "1" if select_clause == "*" else select_clause
            return f"SELECT {select_value}\nWHERE {where_sql}", params

        if len(namespaces) == 1 and self._count_terms(plan) == 1 and not plan.references():
            return self._compile_single_namespace_plan(plan, namespaces[0], mid_value, select_clause, mid_expression, seen_rules)

        from_sql, aliases, ordered_namespaces = self._build_from_join(namespaces)

        if mid_expression:
            mid_sql = self._mid_condition(ordered_namespaces, aliases, mid_expression=mid_expression)
        else:
            mid_sql = self._mid_condition(ordered_namespaces, aliases)
            params.append(mid_value)

        where_sql = self._compile_plan_where(plan, aliases, params, mid_value, mid_expression, seen_rules)

        sql = f"SELECT {select_clause}\n{from_sql}\nWHERE {mid_sql}"
        if where_sql:
            sql += f"\n  AND (\n    {where_sql}\n  )"
        return sql, params

    def _count_terms(self, plan: RulePlan) -> int:
        return sum(len(g.terms) for g in plan.eval_groups)

    def _compile_single_namespace_plan(self, plan, namespace, mid_value, select_clause, mid_expression, seen_rules):
        from_sql, aliases, ordered_namespaces = self._build_from_join([namespace])
        params = []
        where_parts = []
        if mid_expression:
            where_parts.append(self._mid_condition(ordered_namespaces, aliases, mid_expression=mid_expression))
        else:
            where_parts.append(self._mid_condition(ordered_namespaces, aliases))
            params.append(mid_value)
        where_sql = self._compile_plan_where(plan, aliases, params, mid_value, mid_expression, seen_rules)
        if where_sql:
            where_parts.append(where_sql)
        return f"SELECT {select_clause}\n{from_sql}\nWHERE " + "\n  AND ".join(where_parts), params

    def _build_from_join(self, namespaces: list[str]):
        base = self._choose_base_namespace(namespaces)
        ordered = [base] + [ns for ns in namespaces if ns != base]
        aliases = {ns: f"t{i + 1}" for i, ns in enumerate(ordered)}

        base_alias = aliases[base]
        base_table = self._safe_table_name(self.namespace_config.table_name(base, include_database=self.include_database))
        base_keys = self.namespace_config.primary_keys(base)

        parts = [f"FROM {base_table} {base_alias}"]

        for ns in ordered[1:]:
            table = self._safe_table_name(self.namespace_config.table_name(ns, include_database=self.include_database))
            alias = aliases[ns]
            right_keys = self.namespace_config.primary_keys(ns)
            if len(base_keys) != len(right_keys):
                raise ValueError(f"Primary key count mismatch between {base} and {ns}")
            join_cond = [
                f"{base_alias}.{self._safe_identifier(bk)} = {alias}.{self._safe_identifier(rk)}"
                for bk, rk in zip(base_keys, right_keys)
            ]
            parts.append(f"JOIN {table} {alias} ON " + " AND ".join(join_cond))
        return "\n".join(parts), aliases, ordered

    def _choose_base_namespace(self, namespaces):
        for ns in namespaces:
            if self.namespace_config.mid_column(ns):
                return ns
        return namespaces[0]

    def _mid_condition(self, ordered_namespaces, aliases, mid_expression=None):
        for ns in ordered_namespaces:
            mid_column = self.namespace_config.mid_column(ns)
            if mid_column:
                col = f"{aliases[ns]}.{self._safe_identifier(mid_column)}"
                return f"{col} = {mid_expression}" if mid_expression else f"{col} = ?"
        raise ValueError("No referenced namespace has a mid_column configured")

    def _compile_plan_where(self, plan: RulePlan, aliases, params, mid_value=None, mid_expression=None, seen_rules=None):
        group_sql = []
        for group in plan.eval_groups:
            sql = self._compile_group(group, aliases, params, mid_value, mid_expression, seen_rules or set())
            if sql:
                group_sql.append(sql)
        if not group_sql:
            return None
        return f" {plan.op} ".join(group_sql)

    def _compile_group(self, group, aliases, params, mid_value, mid_expression, seen_rules):
        not_equal_preds = [t for t in group.terms if isinstance(t, Predicate) and t.operator == "!="]

        if len(not_equal_preds) >= 2:
            positive = [self._compile_predicate(t, aliases, force_equal=True) for t in not_equal_preds]
            not_block = "NOT (" + " AND ".join(positive) + ")"
            parts = []
            inserted = False
            for term in group.terms:
                if isinstance(term, Predicate) and term.operator == "!=":
                    if not inserted:
                        parts.append(not_block)
                        inserted = True
                else:
                    compiled = self._compile_term(term, aliases, params, mid_value, mid_expression, seen_rules)
                    if compiled:
                        parts.append(compiled)
            return "(" + f" {group.op} ".join(parts) + ")" if parts else None

        parts = []
        for term in group.terms:
            compiled = self._compile_term(term, aliases, params, mid_value, mid_expression, seen_rules)
            if compiled:
                parts.append(compiled)
        return "(" + f" {group.op} ".join(parts) + ")" if parts else None

    def _compile_term(self, term, aliases, params, mid_value, mid_expression, seen_rules):
        if isinstance(term, Predicate):
            return self._compile_predicate(term, aliases)
        if isinstance(term, RuleReference):
            return self._compile_rule_reference(term, aliases, params, mid_value, mid_expression, seen_rules)
        raise ValueError(f"Unknown term: {term}")

    def _compile_rule_reference(self, ref: RuleReference, aliases, params, mid_value, mid_expression, seen_rules):
        if not self.rule_resolver:
            raise ValueError("rule_resolver is required for rule references")
        if ref.rule_name in seen_rules:
            raise ValueError(f"Circular rule reference found: {ref.rule_name}")
        nested_plan = self.rule_resolver.resolve_plan(ref.rule_name)

        if aliases:
            outer_ns = next(iter(aliases))
            outer_mid = self.namespace_config.mid_column(outer_ns) or "mid"
            nested_mid_expression = f"{aliases[outer_ns]}.{self._safe_identifier(outer_mid)}"
            nested_mid_value = None
        else:
            nested_mid_expression = mid_expression
            nested_mid_value = mid_value

        nested_sql, nested_params = self.compile(
            nested_plan,
            mid_value=nested_mid_value,
            select_clause="1",
            mid_expression=nested_mid_expression,
            seen_rules=seen_rules | {ref.rule_name},
        )
        params.extend(nested_params)
        nested_sql = nested_sql.strip().rstrip(";")
        exists_sql = "EXISTS (\n" + indent(nested_sql, "  ") + "\n)"
        return exists_sql if ref.expected_result else "NOT " + exists_sql

    def _compile_predicate(self, pred: Predicate, aliases, force_equal=False):
        if pred.namespace not in aliases:
            raise ValueError(f"No alias for namespace {pred.namespace}")
        col = f"{aliases[pred.namespace]}.{self._safe_identifier(pred.field)}"
        op = "=" if force_equal else pred.operator
        val = pred.value

        if op == "=":
            return f"{col} IS NULL" if val is None else f"{col} = {self._literal(val)}"
        if op == "!=":
            return f"{col} IS NOT NULL" if val is None else f"{col} <> {self._literal(val)}"
        if op in (">", ">=", "<", "<="):
            return f"{col} {op} {self._literal(val)}"
        if op == "contains":
            return f"{col} LIKE '%{str(val).replace("'", "''")}%'"
        if op == "starts_with":
            return f"{col} LIKE '{str(val).replace("'", "''")}%'"
        if op == "ends_with":
            return f"{col} LIKE '%{str(val).replace("'", "''")}'"
        if op in ("in", "has_any", "has_all"):
            values = val if isinstance(val, list) else [val]
            if not values:
                return "1 = 0"
            return f"{col} IN ({', '.join(self._literal(v) for v in values)})"
        if op in ("not_in", "has_none"):
            values = val if isinstance(val, list) else [val]
            if not values:
                return "1 = 1"
            return f"{col} NOT IN ({', '.join(self._literal(v) for v in values)})"
        if op == "exists":
            return f"{col} IS NOT NULL"
        if op == "not_exists":
            return f"{col} IS NULL"
        if op == "is_null":
            return f"{col} IS NULL"
        if op == "is_not_null":
            return f"{col} IS NOT NULL"
        raise ValueError(f"Unsupported operator: {op}")

    def _literal(self, value):
        date_sql = self._relative_date_literal(value)
        if date_sql:
            return date_sql
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            if re.match(r"^-?\d+(\.\d+)?$", value):
                return value
            return "'" + value.replace("'", "''") + "'"
        raise ValueError(f"Unsupported literal: {value}")

    def _relative_date_literal(self, value):
        return None

    def _safe_identifier(self, value: str) -> str:
        if not isinstance(value, str) or not _IDENTIFIER_RE.match(value):
            raise ValueError(f"Invalid SQL identifier: {value}")
        return value

    def _safe_table_name(self, table_name: str) -> str:
        return ".".join(self._safe_identifier(part) for part in table_name.split("."))

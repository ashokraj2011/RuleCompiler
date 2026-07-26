from __future__ import annotations

from collections import OrderedDict
from typing import Any

from .model import EvalGroup, Predicate, RulePlan, RuleReference
from .operators import (
    RULE_METADATA_NAMESPACE,
    expected_result_for_rule_reference,
    normalize_comparison,
    normalize_operator,
)


def _normalize_datasource(value) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower()


def should_skip_term(term: dict[str, Any], skipped_datasources: list[str] | None = None) -> bool:
    if not skipped_datasources:
        return False

    skipped = {_normalize_datasource(ds) for ds in skipped_datasources}
    datasource = term.get("field", {}).get("datasource")
    return _normalize_datasource(datasource) in skipped


def get_rule_name_from_field(field: dict[str, Any]) -> str:
    return (
        field.get("rule")
        or field.get("rule_name")
        or field.get("rule_id")
        or field["name"]
    )


def parse_rule(rule_json: dict[str, Any], skipped_datasources: list[str] | None = None) -> RulePlan:
    """
    Converts user-facing rule JSON into RulePlan IR.

    Semantic choices:
    - same evaluation_group becomes one EvalGroup
    - top-level op links EvalGroups
    - skipped datasource terms are removed before plan creation
    - rulemetadata terms become RuleReference objects
    - no remaining terms means RulePlan(is_always_true=True)
    """
    top_op = normalize_operator(rule_json.get("op", "and"))
    group_map: OrderedDict[str, EvalGroup] = OrderedDict()

    def walk(node: dict[str, Any], parent_op: str):
        current_op = normalize_operator(node.get("op", parent_op))

        for term in node.get("terms", []):
            if "terms" in term:
                walk(term, current_op)
                continue

            if should_skip_term(term, skipped_datasources):
                continue

            field = term["field"]
            group_id = str(field.get("evaluation_group", "default"))

            if group_id not in group_map:
                group_map[group_id] = EvalGroup(id=group_id, op=current_op)

            if group_map[group_id].op != current_op:
                raise ValueError(
                    f"Conflicting operators for evaluation_group {group_id}: "
                    f"{group_map[group_id].op} and {current_op}"
                )

            namespace = field["namespace"]
            datasource = field.get("datasource")

            if namespace == RULE_METADATA_NAMESPACE:
                group_map[group_id].terms.append(
                    RuleReference(
                        rule_name=get_rule_name_from_field(field),
                        expected_result=expected_result_for_rule_reference(
                            term["comp"], term.get("value")
                        ),
                        datasource=datasource,
                        evaluation_group=group_id,
                    )
                )
            else:
                group_map[group_id].terms.append(
                    Predicate(
                        namespace=namespace,
                        field=field["name"],
                        operator=normalize_comparison(term["comp"]),
                        value=term.get("value"),
                        datasource=datasource,
                        evaluation_group=group_id,
                    )
                )

    walk(rule_json, top_op)

    groups = [g for g in group_map.values() if g.terms]
    if not groups:
        return RulePlan(op=top_op, is_always_true=True)

    return RulePlan(op=top_op, eval_groups=groups)

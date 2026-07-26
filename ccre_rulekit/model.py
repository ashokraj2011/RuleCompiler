from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Union

LogicalOp = Literal["AND", "OR"]


@dataclass(frozen=True)
class Predicate:
    namespace: str
    field: str
    operator: str
    value: Any
    datasource: str | None = None
    evaluation_group: str = "default"


@dataclass(frozen=True)
class RuleReference:
    rule_name: str
    expected_result: bool
    datasource: str | None = None
    evaluation_group: str = "default"


PlanTerm = Union[Predicate, RuleReference]


@dataclass
class EvalGroup:
    id: str
    op: LogicalOp
    terms: list[PlanTerm] = field(default_factory=list)


@dataclass
class RulePlan:
    op: LogicalOp
    eval_groups: list[EvalGroup] = field(default_factory=list)
    is_always_true: bool = False

    def namespaces(self) -> list[str]:
        result: list[str] = []
        for group in self.eval_groups:
            for term in group.terms:
                if isinstance(term, Predicate) and term.namespace not in result:
                    result.append(term.namespace)
        return result

    def references(self) -> list[str]:
        result: list[str] = []
        for group in self.eval_groups:
            for term in group.terms:
                if isinstance(term, RuleReference) and term.rule_name not in result:
                    result.append(term.rule_name)
        return result

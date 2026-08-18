from __future__ import annotations

import json

from .parser import parse_rule


class RuleResolver:
    def __init__(self, rule_lookup_df=None, skipped_datasources=None):
        self.rule_lookup_df = rule_lookup_df
        self.skipped_datasources = skipped_datasources or []

    def resolve_json(self, rule_name: str) -> dict:
        if self.rule_lookup_df is None:
            raise ValueError("rule_lookup_df is required for rule references")

        rows = self.rule_lookup_df[
            self.rule_lookup_df["rule"].astype(str) == str(rule_name)
        ]

        if rows.empty:
            raise ValueError(f"Rule not found: {rule_name}")

        rule_def = rows.iloc[0]["rule_def"]

        if isinstance(rule_def, str):
            return json.loads(rule_def)

        return rule_def

    def resolve_plan(self, rule_name: str, seen_rules=None):
        rule_json = self.resolve_json(rule_name)
        return parse_rule(rule_json, skipped_datasources=self.skipped_datasources)

from __future__ import annotations

from .config import NamespaceConfig
from .compilers.postgres import PostgresCompiler
from .compilers.spark_sql import SparkSqlCompiler
from .parser import parse_rule
from .resolver import RuleResolver


class RuleCompiler:
    def __init__(self, namespace_config, rule_lookup_df=None, skipped_datasources=None):
        self.skipped_datasources = skipped_datasources or []
        self.namespace_config = NamespaceConfig(namespace_config)
        self.rule_resolver = None
        if rule_lookup_df is not None:
            self.rule_resolver = RuleResolver(rule_lookup_df, skipped_datasources=self.skipped_datasources)

    def plan(self, rule_json):
        return parse_rule(rule_json, skipped_datasources=self.skipped_datasources)

    def to_postgres_sql(self, rule_json, mid_value=None, select_clause="*"):
        plan = self.plan(rule_json)
        compiler = PostgresCompiler(self.namespace_config, rule_resolver=self.rule_resolver)
        return compiler.compile(plan, mid_value=mid_value, select_clause=select_clause)

    def to_spark_sql(self, rule_json, mid_value=None, select_clause="*", include_database=False):
        plan = self.plan(rule_json)
        compiler = SparkSqlCompiler(
            self.namespace_config,
            rule_resolver=self.rule_resolver,
            include_database=include_database,
        )
        return compiler.compile(plan, mid_value=mid_value, select_clause=select_clause)

    def to_pyspark_dataframe(self, rule_json, raw_frames, mid_value=None, universe_df=None, spark=None):
        from .compilers.pyspark_df import PySparkDataFrameCompiler

        plan = self.plan(rule_json)
        compiler = PySparkDataFrameCompiler(
            self.namespace_config,
            rule_resolver=self.rule_resolver,
            spark=spark,
        )
        return compiler.compile(plan, raw_frames=raw_frames, mid_value=mid_value, universe_df=universe_df)

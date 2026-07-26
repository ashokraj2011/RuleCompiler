import pandas as pd
from ccre_rulekit import RuleCompiler

namespace_config_df = pd.DataFrame([
    {"namespace": "moneyMovementEnriched", "table_name": "money_movement_enriched", "primary_keys": ["mid"], "mid_column": "mid"},
    {"namespace": "aoFundingAccounts", "table_name": "ao_funding_accounts", "primary_keys": ["mid"], "mid_column": "mid"},
    {"namespace": "accountRestrictions", "table_name": "account_restrictions", "primary_keys": ["mid"], "mid_column": "mid"},
])

rule_json = {
    "op": "and",
    "terms": [
        {
            "op": "and",
            "terms": [
                {"comp": "has all of", "field": {"name": "movement_status", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": ["completed", "received"]},
                {"comp": "greater than equal to", "field": {"name": "amount", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": "800"},
            ],
        },
        {
            "op": "and",
            "terms": [
                {"comp": "contains", "field": {"name": "funding_type", "namespace": "aoFundingAccounts", "datasource": "DB", "evaluation_group": "2"}, "value": "TOA SUBMIT"},
                {"comp": "equal to", "field": {"name": "expiration_date", "namespace": "accountRestrictions", "datasource": "DB", "evaluation_group": "3"}, "value": "CURRENT_DATE:ago:8:day(s)"},
            ],
        },
    ],
}

compiler = RuleCompiler(namespace_config_df)

print("--- IR ---")
print(compiler.plan(rule_json))

print("--- Postgres ---")
sql, params = compiler.to_postgres_sql(rule_json, mid_value="12345")
print(sql)
print(params)

print("--- Spark SQL ---")
sql, params = compiler.to_spark_sql(rule_json, mid_value="12345")
print(sql)
print(params)

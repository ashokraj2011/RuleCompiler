import pandas as pd
from cre_rulekit import RuleCompiler


def namespace_config():
    return pd.DataFrame([
        {"namespace": "moneyMovementEnriched", "table_name": "money_movement_enriched", "primary_keys": ["mid"], "mid_column": "mid"},
        {"namespace": "aoFundingAccounts", "table_name": "ao_funding_accounts", "primary_keys": ["mid"], "mid_column": "mid"},
    ])


def test_single_rule_postgres():
    rule = {
        "op": "all",
        "terms": [
            {"comp": "greater than equal to", "field": {"name": "amount", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": "800"}
        ],
    }
    sql, params = RuleCompiler(namespace_config()).to_postgres_sql(rule, mid_value="12345")
    assert "FROM money_movement_enriched t1" in sql
    assert "t1.mid = ?" in sql
    assert "t1.amount >= 800" in sql
    assert params == ["12345"]


def test_skipped_rule_is_true():
    rule = {
        "op": "all",
        "terms": [
            {"comp": "greater than equal to", "field": {"name": "amount", "namespace": "moneyMovementEnriched", "datasource": "CASGraphQL", "evaluation_group": "1"}, "value": "800"}
        ],
    }
    sql, params = RuleCompiler(namespace_config(), skipped_datasources=["CASGraphQL"]).to_postgres_sql(rule, mid_value="12345")
    assert sql == "SELECT now()::date;"
    assert params == []


def test_not_equal_group():
    rule = {
        "op": "and",
        "terms": [
            {"comp": "not equal to", "field": {"name": "status", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": "closed"},
            {"comp": "not equal to", "field": {"name": "type", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": "x"},
        ],
    }
    sql, _ = RuleCompiler(namespace_config()).to_postgres_sql(rule, mid_value="1")
    assert "NOT (t1.status = 'closed' AND t1.type = 'x')" in sql


def test_spark_date():
    rule = {
        "op": "all",
        "terms": [
            {"comp": "equal to", "field": {"name": "expiration_date", "namespace": "moneyMovementEnriched", "datasource": "DB", "evaluation_group": "1"}, "value": "CURRENT_DATE:ago:8:day(s)"}
        ],
    }
    sql, _ = RuleCompiler(namespace_config()).to_spark_sql(rule, mid_value="1")
    assert "date_sub(current_date(), 8)" in sql

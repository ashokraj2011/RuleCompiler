# ccre-rulekit

Small compiler-style library for CCRE rules.

Flow:

```text
Rule JSON -> RulePlan IR -> Postgres SQL / Spark SQL / PySpark DataFrame
```

## Install locally

```bash
pip install -e .
```

## Quick usage

```python
import pandas as pd
from ccre_rulekit import RuleCompiler

namespace_config_df = pd.DataFrame([
    {
        "namespace": "moneyMovementEnriched",
        "table_name": "money_movement_enriched",
        "primary_keys": ["mid"],
        "mid_column": "mid",
    }
])

rule_json = {
    "op": "all",
    "terms": [
        {
            "comp": "greater than equal to",
            "field": {
                "name": "amount",
                "namespace": "moneyMovementEnriched",
                "datasource": "DB",
                "evaluation_group": "1"
            },
            "value": "800"
        }
    ]
}

compiler = RuleCompiler(namespace_config_df)
sql, params = compiler.to_postgres_sql(rule_json, mid_value="12345")
print(sql)
print(params)
```

from __future__ import annotations

from ccre_rulekit.compilers.base_sql import BaseSqlCompiler
from ccre_rulekit.dates import parse_relative_current_date


class PostgresCompiler(BaseSqlCompiler):
    dialect = "postgres"
    true_sql = "SELECT now()::date;"

    def _relative_date_literal(self, value):
        parsed = parse_relative_current_date(value)
        if not parsed:
            return None
        direction, amount, unit = parsed
        operator = "-" if direction == "ago" else "+"
        return f"CURRENT_DATE {operator} INTERVAL '{amount} {unit}'"

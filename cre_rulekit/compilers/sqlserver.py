from __future__ import annotations

from cre_rulekit.compilers.base_sql import BaseSqlCompiler
from cre_rulekit.dates import parse_relative_current_date


class SqlServerCompiler(BaseSqlCompiler):
    dialect = "sqlserver"
    true_sql = "SELECT 1"

    def _relative_date_literal(self, value):
        parsed = parse_relative_current_date(value)
        if not parsed:
            return None
        direction, amount, unit = parsed
        sign = -1 if direction == "ago" else 1

        if unit == "day":
            return f"DATEADD(day, {sign * amount}, CAST(GETDATE() AS date))"
        if unit == "week":
            return f"DATEADD(day, {sign * amount * 7}, CAST(GETDATE() AS date))"
        if unit == "month":
            return f"DATEADD(month, {sign * amount}, CAST(GETDATE() AS date))"
        if unit == "year":
            return f"DATEADD(year, {sign * amount}, CAST(GETDATE() AS date))"
        raise ValueError(f"Unsupported relative date unit: {unit}")

    def _literal(self, value):
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            if value.lower() in {"true", "false"}:
                return "1" if value.lower() == "true" else "0"
            if value.startswith("CURRENT_DATE:"):
                date_sql = self._relative_date_literal(value)
                if date_sql:
                    return date_sql
            if value and value.replace(".", "", 1).replace("-", "", 1).isdigit():
                return value
            return "'" + value.replace("'", "''") + "'"
        raise ValueError(f"Unsupported literal: {value}")

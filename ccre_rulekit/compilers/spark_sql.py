from __future__ import annotations

from ccre_rulekit.compilers.base_sql import BaseSqlCompiler
from ccre_rulekit.dates import parse_relative_current_date


class SparkSqlCompiler(BaseSqlCompiler):
    dialect = "spark"
    true_sql = "SELECT current_date()"

    def _relative_date_literal(self, value):
        parsed = parse_relative_current_date(value)
        if not parsed:
            return None
        direction, amount, unit = parsed
        sign = -1 if direction == "ago" else 1

        if unit == "day":
            return f"date_sub(current_date(), {amount})" if sign < 0 else f"date_add(current_date(), {amount})"
        if unit == "week":
            days = amount * 7
            return f"date_sub(current_date(), {days})" if sign < 0 else f"date_add(current_date(), {days})"
        if unit == "month":
            return f"add_months(current_date(), {sign * amount})"
        if unit == "year":
            return f"add_months(current_date(), {sign * amount * 12})"
        raise ValueError(f"Unsupported relative date unit: {unit}")

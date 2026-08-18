from __future__ import annotations

import re

_RELATIVE_DATE_RE = re.compile(
    r"^CURRENT_DATE:(ago|from_now):(\d+):(day|week|month|year)\(s\)$"
)


def parse_relative_current_date(value: str):
    if not isinstance(value, str):
        return None
    match = _RELATIVE_DATE_RE.match(value)
    if not match:
        return None
    direction, amount, unit = match.groups()
    return direction, int(amount), unit

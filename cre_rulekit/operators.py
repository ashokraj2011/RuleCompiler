RULE_METADATA_NAMESPACE = "rulemetadata"

COMPARISON_MAP = {
    "equal to": "=",
    "not equal to": "!=",
    "greater than": ">",
    "greater than equal to": ">=",
    "less than": "<",
    "less than equal to": "<=",
    "contains": "contains",
    "starts with": "starts_with",
    "ends with": "ends_with",
    "has all of": "has_all",
    "has any of": "has_any",
    "has none of": "has_none",
    "in": "in",
    "not in": "not_in",
    "exists": "exists",
    "not exists": "not_exists",
    "is null": "is_null",
    "is not null": "is_not_null",
}


def normalize_operator(op: str | None) -> str:
    value = (op or "and").lower().strip()

    if value in ("and", "all"):
        return "AND"

    if value in ("or", "any"):
        return "OR"

    raise ValueError(f"Unsupported operator: {op}")


def normalize_comparison(comp: str) -> str:
    key = comp.lower().strip()

    if key not in COMPARISON_MAP:
        raise ValueError(f"Unsupported comparison: {comp}")

    return COMPARISON_MAP[key]


def to_bool(value) -> bool:
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()

    if text == "true":
        return True

    if text == "false":
        return False

    raise ValueError(f"Expected true/false but got: {value}")


def expected_result_for_rule_reference(comp: str, value) -> bool:
    comp_key = comp.lower().strip()
    bool_value = to_bool(value)

    if comp_key == "equal to":
        return bool_value

    if comp_key == "not equal to":
        return not bool_value

    raise ValueError("rulemetadata supports only equal to / not equal to")

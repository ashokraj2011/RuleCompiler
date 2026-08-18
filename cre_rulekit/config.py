from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NamespaceEntry:
    namespace: str
    table_name: str
    primary_keys: list[str]
    mid_column: str | None
    database_name: str | None = None

    @property
    def full_table_name(self) -> str:
        if self.database_name:
            return f"{self.database_name}.{self.table_name}"
        return self.table_name


class NamespaceConfig:
    def __init__(self, config):
        self._entries = self._normalize(config)

    def get(self, namespace: str) -> NamespaceEntry:
        if namespace not in self._entries:
            raise ValueError(f"Missing namespace config for: {namespace}")
        return self._entries[namespace]

    def contains(self, namespace: str) -> bool:
        return namespace in self._entries

    def table_name(self, namespace: str, include_database: bool = False) -> str:
        entry = self.get(namespace)
        return entry.full_table_name if include_database else entry.table_name

    def primary_keys(self, namespace: str) -> list[str]:
        return self.get(namespace).primary_keys

    def mid_column(self, namespace: str) -> str | None:
        return self.get(namespace).mid_column

    def as_dict(self) -> dict[str, NamespaceEntry]:
        return dict(self._entries)

    def _normalize(self, config) -> dict[str, NamespaceEntry]:
        if isinstance(config, NamespaceConfig):
            return config.as_dict()

        if isinstance(config, dict):
            return self._from_dict(config)

        if hasattr(config, "iterrows"):
            return self._from_dataframe(config)

        raise ValueError("namespace_config must be a dict, dataframe, or NamespaceConfig")

    def _from_dict(self, config: dict[str, dict[str, Any]]) -> dict[str, NamespaceEntry]:
        result = {}
        for namespace, row in config.items():
            table_name = row.get("table_name") or row.get("table") or namespace
            primary_keys = row.get("primary_keys") or row.get("primary keys") or row.get("primary_key")
            mid_column = row.get("mid_column")
            database_name = row.get("database_name")
            result[str(namespace)] = NamespaceEntry(
                namespace=str(namespace),
                table_name=str(table_name),
                primary_keys=self._normalize_primary_keys(primary_keys),
                mid_column=None if self._is_missing(mid_column) else str(mid_column),
                database_name=None if self._is_missing(database_name) else str(database_name),
            )
        return result

    def _from_dataframe(self, df) -> dict[str, NamespaceEntry]:
        result = {}
        for _, row in df.iterrows():
            namespace = row.get("namespace")
            if self._is_missing(namespace):
                raise ValueError("namespace_config dataframe requires namespace column")

            table_name = row.get("table_name") if "table_name" in row else row.get("table")
            if self._is_missing(table_name):
                table_name = namespace

            primary_keys = None
            for col in ("primary_keys", "primary keys", "primary_key", "primary key"):
                if col in row and not self._is_missing(row.get(col)):
                    primary_keys = row.get(col)
                    break

            mid_column = row.get("mid_column") if "mid_column" in row else None
            database_name = row.get("database_name") if "database_name" in row else None

            namespace = str(namespace)
            result[namespace] = NamespaceEntry(
                namespace=namespace,
                table_name=str(table_name),
                primary_keys=self._normalize_primary_keys(primary_keys),
                mid_column=None if self._is_missing(mid_column) else str(mid_column),
                database_name=None if self._is_missing(database_name) else str(database_name),
            )
        return result

    def _is_missing(self, value) -> bool:
        if value is None:
            return True
        try:
            return isinstance(value, float) and math.isnan(value)
        except Exception:
            return False

    def _normalize_primary_keys(self, value) -> list[str]:
        if self._is_missing(value):
            raise ValueError("primary_keys is missing")

        if isinstance(value, list):
            return [str(v) for v in value]

        if isinstance(value, (tuple, set)):
            return [str(v) for v in value]

        if isinstance(value, str):
            text = value.strip()
            if not text:
                raise ValueError("primary_keys is empty")
            try:
                parsed = ast.literal_eval(text)
                if isinstance(parsed, (list, tuple, set)):
                    return [str(v) for v in parsed]
                if isinstance(parsed, str):
                    return [parsed]
            except Exception:
                pass
            if "," in text:
                return [p.strip() for p in text.split(",") if p.strip()]
            return [text]

        raise ValueError(f"Invalid primary_keys value: {value}")

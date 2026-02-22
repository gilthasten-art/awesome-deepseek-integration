from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Callable, Iterable, List

from regenerative_dossier_engine.models import FinancialEntry

FinancialChangeCallback = Callable[[], None]


class FinancialSQLiteStore:
    """Tracks auditable financial snapshots in SQLite and emits change events."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._callbacks: List[FinancialChangeCallback] = []
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS financial_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT NOT NULL UNIQUE,
                    revenue REAL NOT NULL,
                    expenses REAL NOT NULL,
                    assets REAL NOT NULL,
                    liabilities REAL NOT NULL,
                    notes TEXT NOT NULL DEFAULT ''
                )
                """
            )

    def subscribe(self, callback: FinancialChangeCallback) -> None:
        self._callbacks.append(callback)

    def _emit_changed(self) -> None:
        for callback in self._callbacks:
            callback()

    def upsert_entry(self, entry: FinancialEntry) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO financial_entries (period, revenue, expenses, assets, liabilities, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(period)
                DO UPDATE SET
                    revenue = excluded.revenue,
                    expenses = excluded.expenses,
                    assets = excluded.assets,
                    liabilities = excluded.liabilities,
                    notes = excluded.notes
                """,
                (entry.period, entry.revenue, entry.expenses, entry.assets, entry.liabilities, entry.notes),
            )
        self._emit_changed()

    def list_entries(self) -> Iterable[FinancialEntry]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT period, revenue, expenses, assets, liabilities, notes
                FROM financial_entries
                ORDER BY period ASC
                """
            ).fetchall()
        return [FinancialEntry(*row) for row in rows]

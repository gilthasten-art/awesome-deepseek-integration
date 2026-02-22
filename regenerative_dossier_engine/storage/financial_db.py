from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Callable

FinancialChangeHandler = Callable[[], None]


class FinancialDatabase:
    """SQLite-backed financial records with change notifications."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._handlers: list[FinancialChangeHandler] = []
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS financial_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT NOT NULL,
                    revenue REAL NOT NULL,
                    expenses REAL NOT NULL,
                    cash_on_hand REAL NOT NULL,
                    liabilities REAL NOT NULL,
                    notes TEXT DEFAULT ''
                )
                """
            )
            conn.commit()

    def register_change_handler(self, handler: FinancialChangeHandler) -> None:
        self._handlers.append(handler)

    def upsert_record(
        self,
        period: str,
        revenue: float,
        expenses: float,
        cash_on_hand: float,
        liabilities: float,
        notes: str = "",
    ) -> None:
        with self._connect() as conn:
            existing = conn.execute(
                "SELECT id FROM financial_records WHERE period = ?", (period,)
            ).fetchone()
            if existing:
                conn.execute(
                    """
                    UPDATE financial_records
                    SET revenue = ?, expenses = ?, cash_on_hand = ?, liabilities = ?, notes = ?
                    WHERE period = ?
                    """,
                    (revenue, expenses, cash_on_hand, liabilities, notes, period),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO financial_records
                    (period, revenue, expenses, cash_on_hand, liabilities, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (period, revenue, expenses, cash_on_hand, liabilities, notes),
                )
            conn.commit()
        self._notify_change()

    def fetch_records(self) -> list[dict[str, float | str]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT period, revenue, expenses, cash_on_hand, liabilities, notes
                FROM financial_records
                ORDER BY period ASC
                """
            ).fetchall()

        return [
            {
                "period": row[0],
                "revenue": row[1],
                "expenses": row[2],
                "cash_on_hand": row[3],
                "liabilities": row[4],
                "notes": row[5],
            }
            for row in rows
        ]

    def _notify_change(self) -> None:
        for handler in self._handlers:
            handler()

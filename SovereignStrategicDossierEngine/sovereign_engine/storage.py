from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period TEXT NOT NULL,
                revenue REAL NOT NULL,
                cost REAL NOT NULL,
                cashflow REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS engine_state (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                input_hash TEXT,
                last_regenerated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.execute(
            """
            INSERT OR IGNORE INTO engine_state(id, input_hash)
            VALUES (1, NULL)
            """
        )
        self.conn.commit()

    def replace_projections(self, rows: list[dict]) -> None:
        self.conn.execute("DELETE FROM projections")
        self.conn.executemany(
            "INSERT INTO projections(period, revenue, cost, cashflow) VALUES(?, ?, ?, ?)",
            [(r["period"], r["revenue"], r["cost"], r["cashflow"]) for r in rows],
        )
        self.conn.commit()

    def fetch_projection_summary(self) -> dict[str, float]:
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(revenue),0), COALESCE(SUM(cost),0), COALESCE(SUM(cashflow),0) FROM projections"
        )
        revenue, cost, cashflow = cur.fetchone()
        margin = ((revenue - cost) / revenue * 100) if revenue else 0.0
        return {
            "total_revenue": revenue,
            "total_cost": cost,
            "total_cashflow": cashflow,
            "operating_margin_pct": margin,
        }

    def get_input_hash(self) -> str | None:
        cur = self.conn.execute("SELECT input_hash FROM engine_state WHERE id = 1")
        row = cur.fetchone()
        return row[0] if row else None

    def set_input_hash(self, value: str) -> None:
        self.conn.execute(
            "UPDATE engine_state SET input_hash = ?, last_regenerated_at = CURRENT_TIMESTAMP WHERE id = 1",
            (value,),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

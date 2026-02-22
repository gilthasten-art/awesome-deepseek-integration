from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import FounderProfile, FinancialProjection, RiskItem, SectorInitiative


class Database:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS founder_profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL,
                background TEXT NOT NULL,
                certifications TEXT NOT NULL,
                governance_focus TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sector_initiatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sector TEXT NOT NULL,
                innovation_thesis TEXT NOT NULL,
                market_strategy TEXT NOT NULL,
                expected_revenue REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS financial_projections (
                year INTEGER PRIMARY KEY,
                revenue REAL NOT NULL,
                cogs REAL NOT NULL,
                opex REAL NOT NULL,
                debt_service REAL NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS risk_register (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                likelihood TEXT NOT NULL,
                impact TEXT NOT NULL,
                mitigation TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS document_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_fingerprint TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                output_manifest TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def upsert_founder(self, founder: FounderProfile) -> None:
        self.conn.execute(
            """
            INSERT INTO founder_profile(id, name, background, certifications, governance_focus)
            VALUES(1, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                background=excluded.background,
                certifications=excluded.certifications,
                governance_focus=excluded.governance_focus,
                updated_at=CURRENT_TIMESTAMP
            """,
            (founder.name, founder.background, founder.certifications, founder.governance_focus),
        )
        self.conn.commit()

    def replace_sectors(self, sectors: Iterable[SectorInitiative]) -> None:
        self.conn.execute("DELETE FROM sector_initiatives")
        self.conn.executemany(
            """
            INSERT INTO sector_initiatives(sector, innovation_thesis, market_strategy, expected_revenue)
            VALUES(?, ?, ?, ?)
            """,
            [(s.sector, s.innovation_thesis, s.market_strategy, s.expected_revenue) for s in sectors],
        )
        self.conn.commit()

    def replace_projections(self, projections: Iterable[FinancialProjection]) -> None:
        self.conn.execute("DELETE FROM financial_projections")
        self.conn.executemany(
            """
            INSERT INTO financial_projections(year, revenue, cogs, opex, debt_service)
            VALUES(?, ?, ?, ?, ?)
            """,
            [(p.year, p.revenue, p.cogs, p.opex, p.debt_service) for p in projections],
        )
        self.conn.commit()

    def replace_risks(self, risks: Iterable[RiskItem]) -> None:
        self.conn.execute("DELETE FROM risk_register")
        self.conn.executemany(
            """
            INSERT INTO risk_register(category, likelihood, impact, mitigation)
            VALUES(?, ?, ?, ?)
            """,
            [(r.category, r.likelihood, r.impact, r.mitigation) for r in risks],
        )
        self.conn.commit()

    def load_founder(self) -> FounderProfile:
        row = self.conn.execute("SELECT * FROM founder_profile WHERE id=1").fetchone()
        if not row:
            raise ValueError("Founder profile is missing")
        return FounderProfile(row["name"], row["background"], row["certifications"], row["governance_focus"])

    def load_sectors(self) -> list[SectorInitiative]:
        rows = self.conn.execute("SELECT * FROM sector_initiatives ORDER BY id").fetchall()
        return [
            SectorInitiative(r["sector"], r["innovation_thesis"], r["market_strategy"], float(r["expected_revenue"]))
            for r in rows
        ]

    def load_projections(self) -> list[FinancialProjection]:
        rows = self.conn.execute("SELECT * FROM financial_projections ORDER BY year").fetchall()
        return [FinancialProjection(r["year"], r["revenue"], r["cogs"], r["opex"], r["debt_service"]) for r in rows]

    def load_risks(self) -> list[RiskItem]:
        rows = self.conn.execute("SELECT * FROM risk_register ORDER BY id").fetchall()
        return [RiskItem(r["category"], r["likelihood"], r["impact"], r["mitigation"]) for r in rows]

    def last_fingerprint(self) -> str | None:
        row = self.conn.execute("SELECT data_fingerprint FROM document_runs ORDER BY id DESC LIMIT 1").fetchone()
        return row[0] if row else None

    def record_document_run(self, data_fingerprint: str, manifest: dict[str, str]) -> None:
        self.conn.execute(
            "INSERT INTO document_runs(data_fingerprint, output_manifest) VALUES(?, ?)",
            (data_fingerprint, json.dumps(manifest)),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

from __future__ import annotations

from pathlib import Path

from regenerative_dossier_engine.engine import RegenerativeDossierEngine
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity


def bootstrap_demo(engine_root: Path) -> None:
    engine = RegenerativeDossierEngine(engine_root)

    founder = FounderIdentity(
        full_name="Jordan Rivers",
        email="jordan@example.com",
        phone="+1-555-0102",
        biography="Founder with 12 years leading finance, logistics, and impact growth initiatives.",
    )
    business = BusinessIdentity(
        legal_name="Regenerative Transit Labs LLC",
        dba_name="RegenTransit",
        ein="12-3456789",
        industry="Clean Mobility",
        mission_statement="Build equitable low-emission transportation infrastructure.",
        address="123 Innovation Ave, Austin, TX",
    )

    engine.save_identity(founder, business)
    engine.record_financial_entry(
        FinancialEntry(period="2025-Q1", revenue=150000, expenses=98000, assets=240000, liabilities=90000)
    )
    engine.record_financial_entry(
        FinancialEntry(period="2025-Q2", revenue=175000, expenses=110000, assets=275000, liabilities=95000)
    )


if __name__ == "__main__":
    bootstrap_demo(Path("./regenerative_workspace"))

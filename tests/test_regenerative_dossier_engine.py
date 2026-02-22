from __future__ import annotations

from pathlib import Path

from regenerative_dossier_engine.engine import RegenerativeDossierEngine
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity


def test_auto_regeneration_creates_outputs(tmp_path: Path) -> None:
    engine = RegenerativeDossierEngine(tmp_path)

    engine.save_identity(
        FounderIdentity(
            full_name="Taylor Green",
            email="taylor@example.com",
            phone="+1-555-1000",
            biography="Operator and founder.",
        ),
        BusinessIdentity(
            legal_name="Green Forge Inc",
            dba_name="GreenForge",
            ein="98-7654321",
            industry="Advanced Manufacturing",
            mission_statement="Decarbonize industrial supply chains.",
            address="44 Harbor St, Boston, MA",
        ),
    )

    engine.record_financial_entry(
        FinancialEntry(period="2025-Q1", revenue=120000, expenses=90000, assets=200000, liabilities=80000)
    )

    assert (tmp_path / "outputs" / "business_profile.docx").exists()
    assert (tmp_path / "outputs" / "business_profile.pdf").exists()
    assert (tmp_path / "outputs" / "sba_loan_packet.docx").exists()
    assert (tmp_path / "outputs" / "grant_narrative.pdf").exists()

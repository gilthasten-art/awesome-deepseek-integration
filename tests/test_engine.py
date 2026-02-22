from pathlib import Path

from regenerative_dossier_engine.engine import RegenerativeDossierEngine


class FakeExporter:
    def export_docx(self, title: str, content: str, output_path: Path) -> Path:
        output_path.write_text(f"DOCX:{title}\n{content}", encoding="utf-8")
        return output_path

    def export_pdf(self, title: str, content: str, output_path: Path) -> Path:
        output_path.write_text(f"PDF:{title}\n{content}", encoding="utf-8")
        return output_path


def test_engine_generates_documents(tmp_path: Path) -> None:
    engine = RegenerativeDossierEngine(tmp_path)
    engine.exporter = FakeExporter()

    engine.set_identity(
        {
            "founder": {"name": "Taylor"},
            "business": {"name": "Nova Works", "industry": "Manufacturing"},
        }
    )
    engine.add_financial_record(
        period="2025-Q1",
        revenue=1000,
        expenses=600,
        cash_on_hand=300,
        liabilities=100,
    )

    results = engine.generate_all(("pdf", "docx"))

    assert "business_profile" in results
    assert (tmp_path / "outputs" / "business_profile.pdf").exists()
    assert (tmp_path / "outputs" / "business_profile.docx").exists()


def test_auto_regeneration_on_financial_change(tmp_path: Path) -> None:
    engine = RegenerativeDossierEngine(tmp_path)
    engine.exporter = FakeExporter()

    engine.set_identity({"founder": {"name": "Taylor"}, "business": {"name": "Nova Works"}})
    engine.enable_auto_regeneration(("pdf",))

    engine.add_financial_record(
        period="2025-Q2",
        revenue=1500,
        expenses=700,
        cash_on_hand=500,
        liabilities=200,
    )

    assert (tmp_path / "outputs" / "grant_narrative.pdf").exists()

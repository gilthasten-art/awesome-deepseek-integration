from __future__ import annotations

from pathlib import Path
from typing import Any

from .exporters.document_exporter import DocumentExporter
from .generation.grant_generator import GrantNarrativeGenerator
from .generation.profile_generator import BusinessProfileGenerator
from .generation.sba_packet_generator import SBALoanPacketGenerator
from .storage.financial_db import FinancialDatabase
from .storage.identity_store import IdentityStore


class RegenerativeDossierEngine:
    """Modular engine for generating and regenerating business dossiers."""

    def __init__(self, workspace: str | Path = "./rde_workspace") -> None:
        self.workspace = Path(workspace)
        self.identity_store = IdentityStore(self.workspace / "identity")
        self.financial_db = FinancialDatabase(self.workspace / "financials.db")
        self.profile_generator = BusinessProfileGenerator()
        self.sba_generator = SBALoanPacketGenerator()
        self.grant_generator = GrantNarrativeGenerator()
        self.exporter = DocumentExporter()
        self.output_dir = self.workspace / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._autogen_enabled = False
        self._last_export_formats: tuple[str, ...] = ("pdf", "docx")
        self.financial_db.register_change_handler(self._on_financial_change)

    def set_identity(self, identity_payload: dict[str, Any]) -> Path:
        return self.identity_store.save(identity_payload)

    def add_financial_record(
        self,
        *,
        period: str,
        revenue: float,
        expenses: float,
        cash_on_hand: float,
        liabilities: float,
        notes: str = "",
    ) -> None:
        self.financial_db.upsert_record(
            period=period,
            revenue=revenue,
            expenses=expenses,
            cash_on_hand=cash_on_hand,
            liabilities=liabilities,
            notes=notes,
        )

    def enable_auto_regeneration(self, formats: tuple[str, ...] = ("pdf", "docx")) -> None:
        self._autogen_enabled = True
        self._last_export_formats = formats

    def disable_auto_regeneration(self) -> None:
        self._autogen_enabled = False

    def generate_all(self, formats: tuple[str, ...] = ("pdf", "docx")) -> dict[str, list[Path]]:
        identity = self.identity_store.load()
        financials = self.financial_db.fetch_records()

        docs = {
            "business_profile": self.profile_generator.generate(identity, financials),
            "sba_loan_packet": self.sba_generator.generate(identity, financials),
            "grant_narrative": self.grant_generator.generate(identity, financials),
        }

        generated_paths: dict[str, list[Path]] = {}
        for doc_name, content in docs.items():
            generated_paths[doc_name] = self._export_document(doc_name, content, formats)
        return generated_paths

    def _export_document(self, doc_name: str, content: str, formats: tuple[str, ...]) -> list[Path]:
        paths: list[Path] = []
        for fmt in formats:
            if fmt == "docx":
                path = self.output_dir / f"{doc_name}.docx"
                paths.append(self.exporter.export_docx(doc_name.replace("_", " ").title(), content, path))
            elif fmt == "pdf":
                path = self.output_dir / f"{doc_name}.pdf"
                paths.append(self.exporter.export_pdf(doc_name.replace("_", " ").title(), content, path))
            else:
                raise ValueError(f"Unsupported export format: {fmt}")
        return paths

    def _on_financial_change(self) -> None:
        if self._autogen_enabled:
            self.generate_all(self._last_export_formats)

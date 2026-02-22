from __future__ import annotations

from pathlib import Path

from regenerative_dossier_engine.generators.grant_generator import GrantNarrativeGenerator
from regenerative_dossier_engine.generators.loan_packet_generator import SBALoanPacketGenerator
from regenerative_dossier_engine.generators.profile_generator import DissertationProfileGenerator
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity
from regenerative_dossier_engine.renderers.document_renderer import StructuredDocumentRenderer
from regenerative_dossier_engine.storage.finance_store import FinancialSQLiteStore
from regenerative_dossier_engine.storage.identity_store import IdentityJSONStore


class RegenerativeDossierEngine:
    """Modular orchestration layer for identity, finance, and auto-generated dossiers."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.identity_store = IdentityJSONStore(root_dir / "data")
        self.finance_store = FinancialSQLiteStore(root_dir / "data" / "financial.db")
        self.renderer = StructuredDocumentRenderer(root_dir / "outputs")

        self.profile_generator = DissertationProfileGenerator()
        self.loan_generator = SBALoanPacketGenerator()
        self.grant_generator = GrantNarrativeGenerator()

        self.finance_store.subscribe(self.regenerate_documents)

    def save_identity(self, founder: FounderIdentity, business: BusinessIdentity) -> None:
        self.identity_store.save(founder, business)

    def record_financial_entry(self, entry: FinancialEntry) -> None:
        self.finance_store.upsert_entry(entry)

    def regenerate_documents(self) -> None:
        founder, business = self.identity_store.load()
        entries = list(self.finance_store.list_entries())

        profile = self.profile_generator.generate(founder, business, entries)
        loan_packet = self.loan_generator.generate(founder, business, entries)
        grant = self.grant_generator.generate(founder, business, entries)

        self.renderer.render(profile, "business_profile")
        self.renderer.render(loan_packet, "sba_loan_packet")
        self.renderer.render(grant, "grant_narrative")

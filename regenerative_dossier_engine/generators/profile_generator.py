from __future__ import annotations

from regenerative_dossier_engine.generators.common import build_dossier, identity_block, summarize_financials
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity


class DissertationProfileGenerator:
    def generate(
        self,
        founder: FounderIdentity,
        business: BusinessIdentity,
        entries: list[FinancialEntry],
    ):
        summary = summarize_financials(entries)
        sections = {
            "Abstract": (
                "This dissertation-grade profile evaluates strategic viability, economic resilience, and "
                "founder-led execution capability through a mixed-method synthesis of identity data and "
                "longitudinal financial records."
            ),
            "Identity and Governance": identity_block(founder, business)
            + f"\nMission Statement: {business.mission_statement}\n\nFounder Biography:\n{founder.biography}",
            "Financial Analysis": (
                f"Total revenue: ${summary['total_revenue']:,.2f}\n"
                f"Total expenses: ${summary['total_expenses']:,.2f}\n"
                f"Net income: ${summary['net_income']:,.2f}\n"
                f"Asset/Liability ratio: {summary['asset_to_liability_ratio']:.2f}"
            ),
            "Strategic Conclusion": (
                "The enterprise demonstrates an operable platform for regenerative growth. "
                "Continuous capitalization and disciplined cost governance are recommended "
                "to improve debt tolerance and qualify for non-dilutive financing instruments."
            ),
        }
        appendices = [f"Financial periods analyzed: {len(entries)}"]
        return build_dossier("Dissertation-Grade Business Profile", sections, appendices)

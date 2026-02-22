from __future__ import annotations

from regenerative_dossier_engine.generators.common import build_dossier, identity_block, summarize_financials
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity


class GrantNarrativeGenerator:
    def generate(self, founder: FounderIdentity, business: BusinessIdentity, entries: list[FinancialEntry]):
        summary = summarize_financials(entries)
        sections = {
            "Need Statement": (
                "The business addresses a documented market and social need while operating with "
                "resource constraints common to early-stage mission-driven ventures."
            ),
            "Organizational Capacity": identity_block(founder, business),
            "Program Narrative": (
                f"With cumulative revenue of ${summary['total_revenue']:,.2f}, the organization has "
                "validated demand and now seeks catalytic grant support to scale impact programming."
            ),
            "Outcomes and Evaluation": (
                "Grant funds will be mapped to measurable outputs, quarterly milestones, and an "
                "evaluation framework linking financial sustainability to community impact indicators."
            ),
        }
        appendices = ["Timeline", "Budget Justification", "Letters of Support"]
        return build_dossier("Grant Narrative", sections, appendices)

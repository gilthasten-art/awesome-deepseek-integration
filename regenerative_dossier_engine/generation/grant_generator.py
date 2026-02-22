from __future__ import annotations

from typing import Any


class GrantNarrativeGenerator:
    """Generates grant-ready narrative content."""

    def generate(self, identity: dict[str, Any], financials: list[dict[str, Any]]) -> str:
        business = identity.get("business", {})
        founder = identity.get("founder", {})
        avg_revenue = (
            sum(item["revenue"] for item in financials) / len(financials) if financials else 0
        )

        return f"""
# Grant Narrative

## Executive Need Statement
{business.get('name', 'The organization')} seeks catalytic funding to scale impact-driven operations in
{business.get('industry', 'its sector')} while strengthening economic resilience in {business.get('location', 'its region')}.

## Founder and Organizational Capability
Led by {founder.get('name', 'the founder')}, the organization combines domain expertise with implementation
capacity, measurable planning discipline, and stakeholder-oriented delivery.

## Program Design and Outcomes
Grant funds will support program expansion, technology enablement, and workforce development.
Expected outcomes include increased service capacity, improved quality benchmarks, and sustainable job creation.

## Financial Stewardship
Average reported revenue: ${avg_revenue:,.2f}. The organization applies transparent bookkeeping,
periodic review controls, and milestone-based budget governance.

## Equity and Community Impact
The proposed work enhances access, affordability, and measurable social benefit across underserved stakeholders.

## Sustainability Plan
Post-grant continuity is underwritten by diversified revenue streams, strategic partnerships, and
tracked performance indicators that guide iterative improvement.
""".strip()

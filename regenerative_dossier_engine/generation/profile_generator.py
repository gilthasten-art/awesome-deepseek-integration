from __future__ import annotations

from typing import Any


class BusinessProfileGenerator:
    """Builds long-form, dissertation-style business profiles."""

    def generate(self, identity: dict[str, Any], financials: list[dict[str, Any]]) -> str:
        founder = identity.get("founder", {})
        business = identity.get("business", {})

        financial_summary = "\n".join(
            [
                (
                    f"- {record['period']}: Revenue ${record['revenue']:,.2f}, "
                    f"Expenses ${record['expenses']:,.2f}, "
                    f"Cash ${record['cash_on_hand']:,.2f}, "
                    f"Liabilities ${record['liabilities']:,.2f}."
                )
                for record in financials
            ]
        ) or "- No financial records available."

        return f"""
# Dissertation-Grade Business Profile

## Abstract
This dossier presents a strategic and operational analysis of {business.get('name', 'the business')}.
It examines leadership competencies, market posture, financial sustainability, and growth pathways.

## Founder Identity and Leadership
Founder: {founder.get('name', 'N/A')}  
Background: {founder.get('background', 'N/A')}  
Core competencies: {founder.get('core_competencies', 'N/A')}

## Business Identity
Legal Name: {business.get('name', 'N/A')}  
Industry: {business.get('industry', 'N/A')}  
Location: {business.get('location', 'N/A')}  
Mission: {business.get('mission', 'N/A')}

## Strategic Analysis
The enterprise demonstrates an adaptive execution model anchored in measurable outcomes and iterative
capital allocation. Differentiation is sustained through founder expertise, customer proximity, and
a disciplined approach to reinvestment.

## Financial Analysis
{financial_summary}

## Risk, Compliance, and Governance
The organization should maintain documented controls for operational risk, financing risk, and
regulatory compliance. Governance maturity can be scaled by adopting quarterly reviews and KPI
surveillance frameworks.

## Conclusion
{business.get('name', 'The business')} is positioned for durable growth with continued financial discipline,
clear capital strategy, and consistent execution against milestone-based plans.
""".strip()

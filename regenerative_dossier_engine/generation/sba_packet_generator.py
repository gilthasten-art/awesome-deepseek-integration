from __future__ import annotations

from typing import Any


class SBALoanPacketGenerator:
    """Generates SBA loan packet narratives and structured sections."""

    def generate(self, identity: dict[str, Any], financials: list[dict[str, Any]]) -> str:
        business = identity.get("business", {})
        founder = identity.get("founder", {})
        latest = financials[-1] if financials else {}

        debt_coverage = "N/A"
        if latest:
            net = latest["revenue"] - latest["expenses"]
            liabilities = latest["liabilities"] or 1
            debt_coverage = f"{net / liabilities:.2f}"

        return f"""
# SBA Loan Packet

## Borrower Information
Business: {business.get('name', 'N/A')}
Founder: {founder.get('name', 'N/A')}
Industry: {business.get('industry', 'N/A')}

## Loan Purpose
Requested capital will be deployed for expansion, working capital stabilization, and process modernization.

## Financial Snapshot
Latest Reporting Period: {latest.get('period', 'N/A')}
Revenue: ${latest.get('revenue', 0):,.2f}
Expenses: ${latest.get('expenses', 0):,.2f}
Cash on Hand: ${latest.get('cash_on_hand', 0):,.2f}
Liabilities: ${latest.get('liabilities', 0):,.2f}
Debt Coverage Indicator: {debt_coverage}

## Repayment Narrative
Repayment is supported by recurring revenue generation, expense controls, and conservative treasury policy.
A monthly cash monitoring process and contingency reserve strategy are built into operating plans.

## Attachments Checklist
- Business profile
- Historical and current financials
- Management bios
- Use-of-funds schedule
- Compliance certifications
""".strip()

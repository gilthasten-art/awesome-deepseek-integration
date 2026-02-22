from __future__ import annotations

from regenerative_dossier_engine.generators.common import build_dossier, identity_block, summarize_financials
from regenerative_dossier_engine.models import BusinessIdentity, FinancialEntry, FounderIdentity


class SBALoanPacketGenerator:
    def generate(self, founder: FounderIdentity, business: BusinessIdentity, entries: list[FinancialEntry]):
        summary = summarize_financials(entries)
        sections = {
            "Borrower Snapshot": identity_block(founder, business),
            "Loan Readiness Analysis": (
                f"Demonstrated gross revenue: ${summary['total_revenue']:,.2f}. "
                f"Net operating position: ${summary['net_income']:,.2f}. "
                "Cashflow discipline and documented operations support SBA underwriting review."
            ),
            "Use of Funds": (
                "Requested funds will be allocated to working capital, hiring, equipment modernization, "
                "and market expansion aligned with mission-critical milestones."
            ),
            "Risk Controls": (
                "Monthly close process, retained earnings policy, and procurement controls are in place "
                "to preserve debt service coverage and borrower compliance."
            ),
        }
        appendices = ["Appendix A: Financial statements", "Appendix B: Ownership documentation"]
        return build_dossier("SBA Loan Packet", sections, appendices)

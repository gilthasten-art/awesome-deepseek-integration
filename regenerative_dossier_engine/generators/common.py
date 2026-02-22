from __future__ import annotations

from datetime import date

from regenerative_dossier_engine.models import BusinessDossier, BusinessIdentity, FinancialEntry, FounderIdentity


def summarize_financials(entries: list[FinancialEntry]) -> dict[str, float]:
    if not entries:
        return {
            "total_revenue": 0.0,
            "total_expenses": 0.0,
            "net_income": 0.0,
            "asset_to_liability_ratio": 0.0,
        }

    total_revenue = sum(x.revenue for x in entries)
    total_expenses = sum(x.expenses for x in entries)
    net_income = total_revenue - total_expenses
    total_assets = sum(x.assets for x in entries)
    total_liabilities = sum(x.liabilities for x in entries)
    ratio = total_assets / total_liabilities if total_liabilities else float(total_assets > 0)
    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_income": net_income,
        "asset_to_liability_ratio": ratio,
    }


def build_dossier(title: str, sections: dict[str, str], appendices: list[str]) -> BusinessDossier:
    return BusinessDossier(
        title=title,
        generated_on=date.today(),
        sections=sections,
        appendices=appendices,
    )


def identity_block(founder: FounderIdentity, business: BusinessIdentity) -> str:
    return (
        f"Founder: {founder.full_name}\n"
        f"Contact: {founder.email} | {founder.phone}\n"
        f"Business: {business.legal_name} ({business.dba_name})\n"
        f"EIN: {business.ein}\nIndustry: {business.industry}\nAddress: {business.address}\n"
    )

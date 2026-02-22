from __future__ import annotations

from .models import DossierBundle


def founder_positioning(bundle: DossierBundle) -> str:
    founder = bundle.founder
    return (
        f"{founder.name} is positioned as a compliance-focused AI infrastructure architect, "
        f"bringing {founder.background}. Credentials: {founder.certifications}. "
        f"Governance doctrine: {founder.governance_focus}."
    )


def dissertation_text(bundle: DossierBundle, risk_index: float, risk_level: str) -> str:
    lines = [
        "Sovereign Strategic Innovation Dissertation",
        "",
        founder_positioning(bundle),
        "",
        "Multi-sector innovation thesis:",
    ]
    for item in bundle.sectors:
        lines.append(
            f"- Sector: {item.sector}. Thesis: {item.innovation_thesis}. "
            f"Go-to-market: {item.market_strategy}. Annual opportunity: ${item.expected_revenue:,.0f}."
        )

    lines.append("")
    lines.append("Financial outlook:")
    for p in bundle.projections:
        ebitda = p.revenue - p.cogs - p.opex
        lines.append(
            f"- {p.year}: revenue ${p.revenue:,.0f}, EBITDA ${ebitda:,.0f}, debt service ${p.debt_service:,.0f}."
        )

    lines.append("")
    lines.append(f"Risk analysis score: {risk_index:.2f} ({risk_level}).")
    lines.append(
        f"Capital readiness: {bundle.assessment.score:.1f}/100 ({bundle.assessment.level}). {bundle.assessment.rationale}"
    )
    return "\n".join(lines)


def sba_loan_packet_text(bundle: DossierBundle) -> str:
    lines = [
        "SBA-Ready Loan Packet",
        "",
        founder_positioning(bundle),
        "",
        "Requested use of proceeds:",
        "- Compliance tooling and audit automation",
        "- Sector-specific deployment infrastructure",
        "- Working capital for enterprise onboarding",
        "",
        f"Capital readiness score: {bundle.assessment.score:.1f} ({bundle.assessment.level})",
        "",
        "Supporting projections:",
    ]
    for p in bundle.projections:
        lines.append(
            f"- FY{p.year}: Revenue ${p.revenue:,.0f} | COGS ${p.cogs:,.0f} | OPEX ${p.opex:,.0f} | Debt Service ${p.debt_service:,.0f}"
        )
    return "\n".join(lines)


def compliance_document_text(bundle: DossierBundle, risk_index: float, risk_level: str) -> str:
    lines = [
        "Compliance & Governance Framework",
        "",
        founder_positioning(bundle),
        "",
        "Governance controls:",
        "- Data lineage and model provenance controls",
        "- Policy-as-code for regulatory control mapping",
        "- Continuous monitoring and incident escalation",
        "",
        "Risk register:",
    ]
    for risk in bundle.risk_register:
        lines.append(
            f"- {risk.category} | Likelihood: {risk.likelihood} | Impact: {risk.impact} | Mitigation: {risk.mitigation}"
        )

    lines.append("")
    lines.append(f"Portfolio risk index: {risk_index:.2f} ({risk_level})")
    lines.append(f"Capital readiness coupling: {bundle.assessment.score:.1f}/100")
    return "\n".join(lines)

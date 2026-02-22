from __future__ import annotations

from statistics import mean

from .models import CapitalAssessment, FinancialProjection, RiskItem


LIKELIHOOD_SCORE = {"low": 1.0, "medium": 2.0, "high": 3.0}
IMPACT_SCORE = {"low": 1.0, "medium": 2.0, "high": 3.0}


def analyze_risk(risks: list[RiskItem]) -> tuple[float, str]:
    if not risks:
        return 0.0, "No declared risks"
    weighted = []
    for risk in risks:
        l = LIKELIHOOD_SCORE.get(risk.likelihood.lower(), 2.0)
        i = IMPACT_SCORE.get(risk.impact.lower(), 2.0)
        weighted.append(l * i)
    risk_index = mean(weighted)
    level = "Low" if risk_index <= 2.0 else "Moderate" if risk_index <= 5.0 else "Elevated"
    return risk_index, level


def capital_readiness_score(projections: list[FinancialProjection], risk_index: float) -> CapitalAssessment:
    if not projections:
        return CapitalAssessment(score=0.0, level="Insufficient Data", rationale="No projections available")

    margins = []
    dscr_values = []
    growth_values = []

    for idx, projection in enumerate(projections):
        gross_margin = max(projection.revenue - projection.cogs, 0) / projection.revenue if projection.revenue else 0
        net_operating = projection.revenue - projection.cogs - projection.opex
        dscr = (net_operating / projection.debt_service) if projection.debt_service else 0
        margins.append(gross_margin)
        dscr_values.append(dscr)
        if idx > 0 and projections[idx - 1].revenue:
            growth_values.append((projection.revenue - projections[idx - 1].revenue) / projections[idx - 1].revenue)

    avg_margin = mean(margins)
    avg_dscr = mean(dscr_values)
    avg_growth = mean(growth_values) if growth_values else 0

    score = 55 + (avg_margin * 20) + (avg_dscr * 10) + (avg_growth * 15) - (risk_index * 4)
    bounded = max(0.0, min(100.0, score))
    level = "Prime" if bounded >= 80 else "Bankable" if bounded >= 65 else "Developing"
    rationale = (
        f"Avg gross margin {avg_margin:.1%}, DSCR {avg_dscr:.2f}, growth {avg_growth:.1%}, "
        f"risk index {risk_index:.2f}."
    )
    return CapitalAssessment(score=bounded, level=level, rationale=rationale)

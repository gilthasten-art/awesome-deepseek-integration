from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class FounderProfile:
    name: str
    background: str
    certifications: str
    governance_focus: str


@dataclass(slots=True)
class SectorInitiative:
    sector: str
    innovation_thesis: str
    market_strategy: str
    expected_revenue: float


@dataclass(slots=True)
class FinancialProjection:
    year: int
    revenue: float
    cogs: float
    opex: float
    debt_service: float


@dataclass(slots=True)
class CapitalAssessment:
    score: float
    level: str
    rationale: str


@dataclass(slots=True)
class RiskItem:
    category: str
    likelihood: str
    impact: str
    mitigation: str


@dataclass(slots=True)
class DossierBundle:
    founder: FounderProfile
    sectors: List[SectorInitiative]
    projections: List[FinancialProjection]
    risk_register: List[RiskItem]
    assessment: CapitalAssessment

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List


@dataclass(slots=True)
class FounderIdentity:
    full_name: str
    email: str
    phone: str
    biography: str


@dataclass(slots=True)
class BusinessIdentity:
    legal_name: str
    dba_name: str
    ein: str
    industry: str
    mission_statement: str
    address: str


@dataclass(slots=True)
class FinancialEntry:
    period: str
    revenue: float
    expenses: float
    assets: float
    liabilities: float
    notes: str = ""


@dataclass(slots=True)
class BusinessDossier:
    title: str
    generated_on: date
    sections: Dict[str, str]
    appendices: List[str]

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .documents import write_docx, write_pdf
from .models import normalize_input
from .scoring import build_risk_report
from .storage import SQLiteStore


class SovereignStrategicDossierEngine:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.store = SQLiteStore(self.output_dir / "sovereign_engine.db")

    def process(self, payload: dict) -> dict[str, str]:
        data = normalize_input(payload)
        digest = hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        self.store.replace_projections(data["financial_projections"])

        prior = self.store.get_input_hash()
        changed = prior != digest

        artifacts: dict[str, str] = {}
        if changed:
            summary = self.store.fetch_projection_summary()
            risk_report = build_risk_report(data["risk_inputs"], summary)
            artifacts = self._generate_all(data, summary, risk_report)
            self.store.set_input_hash(digest)

        return {
            "changed": str(changed),
            "artifacts": json.dumps(artifacts),
        }

    def _generate_all(self, data: dict, summary: dict, risk_report) -> dict[str, str]:
        docs = {
            "founder_positioning": self._founder_sections(data),
            "innovation_dissertation": self._dissertation_sections(data, summary),
            "sba_loan_packet": self._loan_sections(data, summary),
            "compliance_governance": self._compliance_sections(data),
            "risk_and_capital_readiness": self._risk_sections(data, summary, risk_report),
        }

        artifacts: dict[str, str] = {}
        for stem, sections in docs.items():
            docx_path = self.output_dir / f"{stem}.docx"
            pdf_path = self.output_dir / f"{stem}.pdf"
            title = stem.replace("_", " ").title()
            write_docx(docx_path, title, sections)
            write_pdf(pdf_path, title, sections)
            artifacts[f"{stem}_docx"] = str(docx_path)
            artifacts[f"{stem}_pdf"] = str(pdf_path)
        return artifacts

    def _founder_sections(self, data: dict) -> list[tuple[str, str]]:
        p = data["founder_profile"]
        founder = p.get("founder_name", "Founder")
        company = p.get("company_name", "Company")
        highlights = "; ".join(p.get("experience_highlights", []))
        return [
            (
                "Executive Positioning",
                f"{founder} is positioned as a compliance-focused AI infrastructure architect at {company}, "
                f"driving governance-first growth in regulated markets.",
            ),
            ("Mission Narrative", p.get("mission", "")),
            ("Credibility Proof Points", highlights),
        ]

    def _dissertation_sections(self, data: dict, summary: dict) -> list[tuple[str, str]]:
        b = data["business_strategy"]
        sectors = ", ".join(b.get("sectors", []))
        offerings = ", ".join(b.get("core_offerings", []))
        milestones = "; ".join(b.get("milestones", []))
        return [
            ("Multi-Sector Thesis", f"Primary sectors: {sectors}. Core offerings: {offerings}."),
            ("Innovation Model", b.get("go_to_market", "")),
            (
                "Economic Scalability",
                f"Projected total revenue: {summary['total_revenue']:.2f}; operating margin: {summary['operating_margin_pct']:.2f}%.",
            ),
            ("Execution Milestones", milestones),
        ]

    def _loan_sections(self, data: dict, summary: dict) -> list[tuple[str, str]]:
        l = data["loan_request"]
        proceeds = l.get("use_of_proceeds", {})
        use_rows = ", ".join(f"{k}: ${v:,.0f}" for k, v in proceeds.items())
        return [
            (
                "Loan Request Summary",
                f"Requested amount: ${float(l.get('requested_amount', 0)):,.0f}; term: {l.get('term_months', 0)} months.",
            ),
            ("Use of Proceeds", use_rows),
            ("Repayment Strategy", l.get("repayment_strategy", "")),
            (
                "Debt Service Confidence",
                f"Projected cumulative cashflow: ${summary['total_cashflow']:,.2f}.",
            ),
        ]

    def _compliance_sections(self, data: dict) -> list[tuple[str, str]]:
        c = data["compliance"]
        return [
            ("Regulatory Scope", ", ".join(c.get("jurisdictions", []))),
            ("Standards Alignment", ", ".join(c.get("standards", []))),
            ("Policy Library", "; ".join(c.get("policies", []))),
            ("Control Framework", "; ".join(c.get("controls", []))),
        ]

    def _risk_sections(self, data: dict, summary: dict, risk_report) -> list[tuple[str, str]]:
        mitigations = "; ".join(data["risk_inputs"].get("mitigations", []))
        return [
            (
                "Risk Analysis",
                f"Overall risk score: {risk_report.overall_risk_score}/100. Mitigations: {mitigations}",
            ),
            (
                "Capital Readiness",
                f"Capital readiness score: {risk_report.capital_readiness_score}/100. {risk_report.narrative}",
            ),
            (
                "Financial Stability Signals",
                f"Total cashflow: ${summary['total_cashflow']:,.2f}; margin: {summary['operating_margin_pct']:.2f}%.",
            ),
        ]

    def close(self) -> None:
        self.store.close()

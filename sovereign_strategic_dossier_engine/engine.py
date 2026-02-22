from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .analytics import analyze_risk, capital_readiness_score
from .database import Database
from .document_builder import DocumentBuilder
from .models import DossierBundle, FinancialProjection, FounderProfile, RiskItem, SectorInitiative
from .templates import compliance_document_text, dissertation_text, sba_loan_packet_text


class SovereignStrategicDossierEngine:
    def __init__(self, db_path: str | Path = "sovereign_dossier.db", output_dir: str | Path = "generated_docs") -> None:
        self.database = Database(db_path)
        self.builder = DocumentBuilder(output_dir)

    def save_inputs(
        self,
        founder: FounderProfile,
        sectors: list[SectorInitiative],
        projections: list[FinancialProjection],
        risks: list[RiskItem],
        force_regenerate: bool = False,
    ) -> dict[str, str]:
        self.database.upsert_founder(founder)
        self.database.replace_sectors(sectors)
        self.database.replace_projections(projections)
        self.database.replace_risks(risks)
        return self.regenerate_documents(force=force_regenerate)

    def build_bundle(self) -> tuple[DossierBundle, float, str]:
        founder = self.database.load_founder()
        sectors = self.database.load_sectors()
        projections = self.database.load_projections()
        risks = self.database.load_risks()

        risk_index, risk_level = analyze_risk(risks)
        assessment = capital_readiness_score(projections, risk_index)
        bundle = DossierBundle(
            founder=founder,
            sectors=sectors,
            projections=projections,
            risk_register=risks,
            assessment=assessment,
        )
        return bundle, risk_index, risk_level

    def regenerate_documents(self, force: bool = False) -> dict[str, str]:
        bundle, risk_index, risk_level = self.build_bundle()
        fingerprint = self._fingerprint(bundle, risk_index, risk_level)
        last = self.database.last_fingerprint()

        if (not force) and last == fingerprint:
            return {"status": "no_changes", "fingerprint": fingerprint}

        dissertation = dissertation_text(bundle, risk_index, risk_level)
        loan_packet = sba_loan_packet_text(bundle)
        compliance = compliance_document_text(bundle, risk_index, risk_level)

        manifest = {
            "dissertation_pdf": str(
                self.builder.write_pdf("Innovation Dissertation", dissertation, "innovation_dissertation.pdf")
            ),
            "dissertation_docx": str(
                self.builder.write_docx("Innovation Dissertation", dissertation, "innovation_dissertation.docx")
            ),
            "sba_packet_pdf": str(self.builder.write_pdf("SBA Loan Packet", loan_packet, "sba_loan_packet.pdf")),
            "sba_packet_docx": str(self.builder.write_docx("SBA Loan Packet", loan_packet, "sba_loan_packet.docx")),
            "compliance_pdf": str(
                self.builder.write_pdf("Compliance Governance", compliance, "compliance_governance.pdf")
            ),
            "compliance_docx": str(
                self.builder.write_docx("Compliance Governance", compliance, "compliance_governance.docx")
            ),
            "risk_index": f"{risk_index:.2f}",
            "capital_readiness_score": f"{bundle.assessment.score:.1f}",
            "capital_readiness_level": bundle.assessment.level,
        }
        self.database.record_document_run(fingerprint, manifest)
        return manifest

    def _fingerprint(self, bundle: DossierBundle, risk_index: float, risk_level: str) -> str:
        payload = {
            "founder": asdict(bundle.founder),
            "sectors": [asdict(s) for s in bundle.sectors],
            "projections": [asdict(p) for p in bundle.projections],
            "risks": [asdict(r) for r in bundle.risk_register],
            "risk_index": risk_index,
            "risk_level": risk_level,
            "assessment": asdict(bundle.assessment),
        }
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def close(self) -> None:
        self.database.close()

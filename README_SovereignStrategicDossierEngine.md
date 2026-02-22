# SovereignStrategicDossierEngine

SovereignStrategicDossierEngine is a production-grade Python system for positioning a founder as a **compliance-focused AI infrastructure architect** while generating lender- and governance-ready documentation.

## Capabilities

- Multi-sector innovation dissertation generation.
- SBA-ready loan packet generation.
- Compliance and governance framework documentation.
- Financial projection persistence and tracking in SQLite.
- Capital readiness scoring and risk analysis.
- Formatted **PDF + DOCX** exports.
- Deterministic document regeneration whenever source data changes.

## Installation

```bash
python -m pip install -e .
```

## Usage

```bash
sovereign-dossier examples/sample_payload.json --db sovereign_dossier.db --output generated_docs
```

To force regeneration:

```bash
sovereign-dossier examples/sample_payload.json --force
```

## Data Model

The input payload requires:

- `founder`
- `sectors`
- `projections`
- `risks`

See `examples/sample_payload.json` for a complete schema sample.

## Generated Outputs

- `innovation_dissertation.pdf` + `.docx`
- `sba_loan_packet.pdf` + `.docx`
- `compliance_governance.pdf` + `.docx`

The SQLite database stores profiles, sector initiatives, risk register items, financial projections, and document-run fingerprints for change detection.

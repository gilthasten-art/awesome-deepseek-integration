# SovereignStrategicDossierEngine

SovereignStrategicDossierEngine is a production-oriented Python system for founders who want to position themselves as compliance-focused AI infrastructure architects while preparing institution-ready business and financing documentation.

## Capabilities

- Founder narrative positioning as a compliance-focused AI infrastructure architect.
- Multi-sector innovation dissertation generation.
- SBA-ready loan packet generation.
- Compliance and governance documentation generation.
- Financial projection persistence and analytics in SQLite.
- Risk analysis and capital readiness scoring.
- DOCX and PDF output for all generated documents.
- Full document regeneration when input data changes.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create an input file (see `sample_input.json`) and run:

```bash
sovereign-dossier --input sample_input.json --output-dir output
```

## Input schema (JSON)

Top-level keys:
- `founder_profile`: founder and company positioning data.
- `business_strategy`: sectors, offerings, go-to-market, milestones.
- `loan_request`: funding goals, use of proceeds, debt profile.
- `compliance`: controls, policies, jurisdictions, standards.
- `financial_projections`: list of period-based revenue/cost/cashflow rows.
- `risk_inputs`: market, regulatory, technology, and execution risk signals.

See `sample_input.json` for a complete example.

## Outputs

The engine writes each artifact as both `.docx` and `.pdf`:
- `founder_positioning`
- `innovation_dissertation`
- `sba_loan_packet`
- `compliance_governance`
- `risk_and_capital_readiness`

A SQLite DB is created at `<output-dir>/sovereign_engine.db` with projection and run metadata tables.

# RegenerativeDossierEngine

A local modular Python system that:

- Stores founder and business identity data in JSON
- Tracks financial data in SQLite
- Generates dissertation-grade business profiles
- Produces SBA loan packets
- Generates grant narratives
- Outputs structured PDF and DOCX files
- Regenerates documents automatically when financial data changes

## Install

```bash
pip install -r regenerative_dossier_engine/requirements.txt
```

## Run demo

```bash
python -m regenerative_dossier_engine.main
```

This creates `regenerative_workspace/` with:

- `data/identity.json`
- `data/financial.db`
- `outputs/business_profile.pdf` and `.docx`
- `outputs/sba_loan_packet.pdf` and `.docx`
- `outputs/grant_narrative.pdf` and `.docx`

## Architecture

- `storage/identity_store.py`: JSON persistence for founder + business identity
- `storage/finance_store.py`: SQLite persistence and change-event subscription
- `generators/*`: domain-specific dossier generators
- `renderers/document_renderer.py`: structured PDF + DOCX rendering
- `engine.py`: orchestration and automatic regeneration workflow

# RegenerativeDossierEngine

RegenerativeDossierEngine is a local modular Python system that:

- Stores founder and business identity data in JSON.
- Tracks financial data in SQLite.
- Generates dissertation-grade business profiles.
- Produces SBA loan packets.
- Generates grant narratives.
- Exports structured PDF and DOCX files.
- Automatically regenerates documents whenever financial records are updated.

## Architecture

- `regenerative_dossier_engine/storage/identity_store.py`: JSON identity persistence.
- `regenerative_dossier_engine/storage/financial_db.py`: SQLite store + change events.
- `regenerative_dossier_engine/generation/profile_generator.py`: dissertation-grade profile writer.
- `regenerative_dossier_engine/generation/sba_packet_generator.py`: SBA loan packet writer.
- `regenerative_dossier_engine/generation/grant_generator.py`: grant narrative writer.
- `regenerative_dossier_engine/exporters/document_exporter.py`: PDF and DOCX exporters.
- `regenerative_dossier_engine/engine.py`: orchestration, modular composition, and auto-regeneration.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```python
from regenerative_dossier_engine import RegenerativeDossierEngine

engine = RegenerativeDossierEngine("./rde_workspace")

engine.set_identity(
    {
        "founder": {
            "name": "Avery Stone",
            "background": "Former operations leader in clean-tech manufacturing",
            "core_competencies": "Operations, financing, and go-to-market execution",
        },
        "business": {
            "name": "HelioForge Labs",
            "industry": "Sustainable energy systems",
            "location": "Austin, TX",
            "mission": "Scale practical energy resilience for SMEs",
        },
    }
)

engine.enable_auto_regeneration(("pdf", "docx"))

engine.add_financial_record(
    period="2025-Q1",
    revenue=420000,
    expenses=280000,
    cash_on_hand=170000,
    liabilities=85000,
    notes="Expansion quarter",
)

# You can also generate manually
paths = engine.generate_all(("pdf", "docx"))
print(paths)
```

Generated files will be written to `rde_workspace/outputs`.

from __future__ import annotations

from pathlib import Path
import sys
import types

if "docx" not in sys.modules:
    sys.modules["docx"] = types.SimpleNamespace(Document=lambda: None)

from sovereign_strategic_dossier_engine.document_builder import DocumentBuilder


class FakeCanvas:
    def __init__(self, *_args, **_kwargs) -> None:
        self.drawn: list[str] = []

    def setFont(self, *_args, **_kwargs) -> None:  # noqa: N802
        return

    def drawString(self, _x: int, _y: int, text: str) -> None:  # noqa: N802
        self.drawn.append(text)

    def showPage(self) -> None:  # noqa: N802
        return

    def save(self) -> None:
        return


def test_write_pdf_wraps_long_lines_without_truncating(monkeypatch, tmp_path: Path) -> None:
    created_canvases: list[FakeCanvas] = []

    def fake_canvas_factory(*_args, **_kwargs) -> FakeCanvas:
        canvas = FakeCanvas()
        created_canvases.append(canvas)
        return canvas

    monkeypatch.setattr("sovereign_strategic_dossier_engine.document_builder.canvas.Canvas", fake_canvas_factory)

    long_line = " ".join(["compliance-first"] * 30)
    builder = DocumentBuilder(tmp_path)
    builder.write_pdf("Title", long_line, "wrapped.pdf")

    assert created_canvases, "Expected DocumentBuilder to instantiate a Canvas"
    rendered_lines = created_canvases[0].drawn
    assert rendered_lines[0] == "Title"
    wrapped_body = rendered_lines[1:]
    assert len(wrapped_body) > 1
    assert "".join(wrapped_body).replace(" ", "") == long_line.replace(" ", "")

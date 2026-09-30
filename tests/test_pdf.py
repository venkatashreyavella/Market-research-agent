from pathlib import Path
from app.pdf.generator import generate_pdf


def test_pdf_generation(monkeypatch):
    tmp_path = Path("output/test-pdf")
    tmp_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("app.pdf.generator.OUTPUT_DIR", tmp_path)
    path = generate_pdf("# Test\n\n## Executive Summary\nHello", "Test Market")
    assert Path(path).exists() and Path(path).read_bytes().startswith(b"%PDF")

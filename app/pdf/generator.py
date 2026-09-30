from pathlib import Path
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from app.config import OUTPUT_DIR


def _safe_name(value): return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")[:80] or "report"


def generate_pdf(markdown: str, subject: str) -> Path:
    path = OUTPUT_DIR / f"{_safe_name(subject)}_market_research.pdf"
    styles = getSampleStyleSheet(); story = []
    story.append(Paragraph("Automated Market Research Report", styles["Title"])); story.append(Paragraph(subject, styles["Heading2"])); story.append(Spacer(1, .25 * inch))
    for line in markdown.splitlines():
        if not line.strip(): story.append(Spacer(1, 6)); continue
        if line.startswith("# "): style = styles["Title"]; text = line[2:]
        elif line.startswith("## "): style = styles["Heading2"]; text = line[3:]
        elif line.startswith("- "): style = styles["BodyText"]; text = "• " + line[2:]
        elif line.startswith("|"): continue
        else: style = styles["BodyText"]; text = line
        story.append(Paragraph(text.replace("&", "&amp;"), style)); story.append(Spacer(1, 4))
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Helvetica", 8); canvas.drawString(.7*inch, .45*inch, "Automated Market Research Agent"); canvas.drawRightString(7.8*inch, .45*inch, f"Page {doc.page}"); canvas.restoreState()
    SimpleDocTemplate(str(path), pagesize=letter, rightMargin=.7*inch, leftMargin=.7*inch, topMargin=.7*inch, bottomMargin=.7*inch).build(story, onFirstPage=footer, onLaterPages=footer)
    return path


from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def generate_pdf(report: str) -> bytes:
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#14243A"),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#244B70"),
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = styles["BodyText"]
    body_style.leading = 15

    story = [
        Paragraph("INDUSTRIAL SPEECH INTELLIGENCE", title_style),
        Paragraph("Compte rendu de maintenance", heading_style),
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#244B70"),
        ),
        Spacer(1, 15),
    ]

    for line in report.splitlines():
        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        safe_line = escape(line)

        if line.startswith("## "):
            story.append(
                Paragraph(escape(line[3:]), heading_style)
            )

        elif line.startswith("# "):
            story.append(
                Paragraph(escape(line[2:]), title_style)
            )

        elif line.startswith("- "):
            story.append(
                Paragraph("• " + escape(line[2:]), body_style)
            )

        else:
            story.append(
                Paragraph(safe_line, body_style)
            )

    document.build(story)

    return buffer.getvalue()

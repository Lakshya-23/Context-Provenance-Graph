"""PDF generation script for demo Revenue Policy documents.

Run this once to create revenue_policy_v1_2.pdf and revenue_policy_v1_3.pdf.

Usage:
    uv run python demo/generate_pdfs.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


SECTIONS_V1_2 = [
    {
        "heading": "1. Revenue Recognition",
        "body": [
            "Revenue is recognized when an order has been fulfilled.",
            "A fulfilled order is an order for which the customer has received the purchased product or service.",
            "Cancelled orders that have not been fulfilled do not generate recognized revenue.",
        ],
    },
    {
        "heading": "2. Refunds",
        "body": [
            "Refunds are amounts returned to customers after a completed transaction.",
            "Refunds processed before settlement are excluded from recognized revenue.",
            "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
        ],
    },
    {
        "heading": "3. Chargebacks",
        "body": [
            "A chargeback is a disputed card transaction initiated by a customer through their payment provider.",
            "Chargebacks are treated as a financial loss associated with the original transaction.",
            "Chargebacks are tracked separately from recognized revenue.",
        ],
    },
    {
        "heading": "4. Revenue Metrics",
        "body": [
            "Gross Revenue represents the value of fulfilled orders before refund adjustments.",
            "Net Revenue represents Gross Revenue less applicable refunds and chargeback losses used for management reporting.",
            "Realized Revenue represents recognized revenue after applicable refund adjustments.",
        ],
    },
    {
        "heading": "5. Reporting Rules",
        "body": [
            "Revenue reporting uses fulfilled orders as the recognition event.",
            "Refunds and chargebacks must be distinguished because they have different accounting and reporting implications.",
        ],
    },
]


# v1.3 changes only section 2 (Refunds)
SECTIONS_V1_3_REFUNDS = {
    "heading": "2. Refunds",
    "body": [
        "Refunds are amounts returned to customers after a completed transaction.",
        "Refunds processed within 30 days of fulfillment are excluded from recognized revenue.",
        "Refunds processed after 30 days are recorded separately and do not reduce reported revenue.",
        "Refunds processed after settlement are recorded separately and do not change the original fulfillment event.",
    ],
}


def _build_styles():
    """Create the document styles."""
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            "DocTitle",
            parent=styles["Title"],
            fontSize=22,
            spaceAfter=4,
            textColor=HexColor("#1a1a2e"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=12,
            spaceAfter=2,
            textColor=HexColor("#555555"),
            fontName="Helvetica",
        )
    )
    styles.add(
        ParagraphStyle(
            "VersionLabel",
            parent=styles["Normal"],
            fontSize=10,
            spaceAfter=20,
            textColor=HexColor("#888888"),
            fontName="Helvetica-Oblique",
        )
    )
    styles.add(
        ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceBefore=18,
            spaceAfter=8,
            textColor=HexColor("#1a1a2e"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            "BodyText2",
            parent=styles["Normal"],
            fontSize=10.5,
            spaceAfter=6,
            leading=15,
            textColor=HexColor("#333333"),
            fontName="Helvetica",
        )
    )
    return styles


def _generate_pdf(filepath: str, version: str, sections: list[dict]):
    """Generate a single PDF document."""
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )
    styles = _build_styles()
    story = []

    # Title block
    story.append(Paragraph("ACME COMMERCE", styles["DocTitle"]))
    story.append(Paragraph("Revenue Recognition Policy", styles["DocSubtitle"]))
    story.append(Paragraph(f"Version: {version}", styles["VersionLabel"]))
    story.append(
        HRFlowable(
            width="100%", thickness=1, color=HexColor("#cccccc"), spaceAfter=12
        )
    )
    story.append(Spacer(1, 8))

    # Sections
    for section in sections:
        story.append(Paragraph(section["heading"], styles["SectionHeading"]))
        for line in section["body"]:
            story.append(Paragraph(line, styles["BodyText2"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    print(f"Created {filepath}")


def generate_v1_2(output_dir: str):
    """Generate Revenue Policy v1.2."""
    filepath = os.path.join(output_dir, "revenue_policy_v1_2.pdf")
    _generate_pdf(filepath, "1.2", SECTIONS_V1_2)
    return filepath


def generate_v1_3(output_dir: str):
    """Generate Revenue Policy v1.3 with changed refund rule."""
    sections = []
    for s in SECTIONS_V1_2:
        if s["heading"] == "2. Refunds":
            sections.append(SECTIONS_V1_3_REFUNDS)
        else:
            sections.append(s)
    filepath = os.path.join(output_dir, "revenue_policy_v1_3.pdf")
    _generate_pdf(filepath, "1.3", sections)
    return filepath


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    v12 = generate_v1_2(script_dir)
    v13 = generate_v1_3(script_dir)

    # Copy both PDFs to public/ for frontend display & download
    public_dir = os.path.join(script_dir, "..", "..", "public")
    os.makedirs(public_dir, exist_ok=True)
    import shutil
    shutil.copy2(v12, os.path.join(public_dir, "revenue_policy_v1_2.pdf"))
    shutil.copy2(v13, os.path.join(public_dir, "revenue_policy_v1_3.pdf"))
    shutil.copy2(v12, os.path.join(public_dir, "Revenue_Policy.pdf"))
    print(f"Copied both v1.2 and v1.3 PDFs to {public_dir}")

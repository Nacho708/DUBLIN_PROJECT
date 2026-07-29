"""
Defines all visual styles used in the PDF.
"""

from reportlab.lib.colors import HexColor

from pdf_generator.config import (
    TITLE_FONT,
    SECTION_FONT,
    LABEL_FONT,
    TITLE_SIZE,
    SECTION_SIZE,
    LABEL_SIZE
)


class PDFStyles:

    def __init__(self, canvas):

        self.canvas = canvas

    # =====================================================
    # TITLES
    # =====================================================

    def draw_title(self, text, x, y):

        self.canvas.setFont(TITLE_FONT, TITLE_SIZE)

        self.canvas.setFillColor(HexColor("#1F4E79"))

        self.canvas.drawString(x, y, text)

    # =====================================================
    # SECTION
    # =====================================================

    def draw_section(self, text, x, y, width):

        self.canvas.setFont(SECTION_FONT, SECTION_SIZE)

        self.canvas.setFillColor(HexColor("#1F4E79"))

        self.canvas.drawString(x, y, text)

        self.canvas.setStrokeColor(HexColor("#1F4E79"))

        self.canvas.setLineWidth(1)

        self.canvas.line(
            x,
            y - 3,
            x + width,
            y - 3
        )

    # =====================================================
    # LABEL
    # =====================================================

    def draw_label(self, text, x, y):

        self.canvas.setFont(LABEL_FONT, LABEL_SIZE)

        self.canvas.setFillColor(HexColor("#000000"))

        self.canvas.drawString(x, y, text)

    # =====================================================
    # FOOTER
    # =====================================================

    def draw_footer(self, page_number, x, y):

        self.canvas.setFont("Helvetica", 8)

        self.canvas.setFillColor(HexColor("#666666"))

        self.canvas.drawRightString(
            x,
            y,
            f"Page {page_number}"
        )
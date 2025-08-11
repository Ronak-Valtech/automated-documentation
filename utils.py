from fpdf import FPDF
import os

FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")
FONT_REGULAR = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")

class TSDPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.add_font("DejaVu", "", FONT_REGULAR, uni=True)
        self.add_font("DejaVu", "B", FONT_BOLD, uni=True)
        self.set_font("DejaVu", size=12)

    def section_title(self, title):
        self.set_font("DejaVu", style="B", size=14)
        self.set_text_color(0, 0, 128)
        self.multi_cell(0, 10, txt=title)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def section_body(self, body):
        self.set_font("DejaVu", size=11)
        self.multi_cell(0, 8, txt=body)
        self.ln(2)

def save_tsd_as_pdf(markdown_text, output_path="data/output_TSD.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf = TSDPDF()

    sections = markdown_text.strip().split("## ")
    for section in sections:
        if section.strip():
            lines = section.strip().split("\n", 1)
            title = lines[0].strip("#").strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            pdf.section_title(title)
            pdf.section_body(body)

    pdf.output(output_path)
    print(f" PDF TSD written to: {output_path}")
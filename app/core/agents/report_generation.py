import os
import uuid
from datetime import datetime
import re
import matplotlib
from fpdf import FPDF
from app.core.state import ReportState

# Ensure a non-interactive backend is used for matplotlib
matplotlib.use('Agg')

def clean_text_for_pdf(text: str) -> str:
    text = text.replace('**', '').replace('*', '')
    return text.strip()

class PDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Data Analysis Report', 0, 0, 'C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def report_generation_node(state: ReportState) -> dict:
    print("\n==========================================")
    print(">>> In Report Generation Node")
    print("============================================")

    report_content = state['report_content']
    
    # Use the plots_path to determine the session's base directory for the output
    session_path = os.path.dirname(state['plots_path'])
    pdf_path = os.path.join(session_path, "financial_analysis_report.pdf")

    pdf = PDF()
    # Title Page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 80, 'Agentic Data Analysis Report', 0, 1, 'C')
    pdf.set_font('Arial', '', 16)
    pdf.cell(0, 20, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", 0, 1, 'C')
    
    pdf.add_page()

    for content in report_content:
        cleaned_analysis_name = clean_text_for_pdf(content.get('analysis_name', 'Unnamed Analysis'))
        cleaned_narrative = clean_text_for_pdf(content.get('narrative', 'No narrative provided.'))
        original_result = content.get('original_result')

        pdf.set_font("Arial", 'B', size=16)
        pdf.multi_cell(0, 10, txt=cleaned_analysis_name, align='L')
        pdf.ln(2)

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, txt=cleaned_narrative)
        pdf.ln(5)

        if isinstance(original_result, str) and original_result.lower().endswith('.png') and os.path.exists(original_result):
            page_width = pdf.w - 2 * pdf.l_margin
            img_width = page_width * 0.9
            x_pos = (pdf.w - img_width) / 2
            pdf.image(original_result, x=x_pos, w=img_width)
            pdf.ln(5)
        
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
        pdf.ln(10)

    pdf.output(pdf_path)
    print(f"PDF report generated successfully at: {pdf_path}")
    
    state['pdf_path'] = pdf_path
    return state


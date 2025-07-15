import markdown
import pdfkit
import os
from datetime import datetime

# Adjust path to your wkhtmltopdf binary
PDFKIT_PATH = "/usr/bin/wkhtmltopdf"

config = pdfkit.configuration(wkhtmltopdf=PDFKIT_PATH)

def generate_pdf(md_text):
    html_body = markdown.markdown(md_text)

    with open("templates/resume_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{CONTENT}}", html_body)

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"output/resume_{timestamp}.pdf"

    pdfkit.from_string(final_html, output_path, configuration=config)
    return output_path

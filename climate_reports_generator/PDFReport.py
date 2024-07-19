import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class PDFReport:
    def __init__(self, user_name):
        # Create an in-memory bytes buffer and a canvas with A4 page size.
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.user_name = user_name
        self.today_date = datetime.datetime.today().date().strftime("%d-%m-%Y")
        self.add_header()

    def add_text(self, text, position, font_size=12):
        # Add regular text to the canvas.
        self.canvas.setFont("Helvetica", font_size)
        self.canvas.drawString(position[0], position[1], text)

    def add_bold_text(self, text, position, font_size=12):
        # Add bold text to the canvas.
        self.canvas.setFont("Helvetica-Bold", font_size)
        self.canvas.drawString(position[0], position[1], text)

    def add_header(self):
        # Add the default header
        darkblue = colors.Color(5/255, 55/255, 95/255)
        self.canvas.setFillColor(darkblue)
        self.canvas.rect(0, self.height - 40, self.width, 40, fill=1, stroke=0)

        yellow = colors.Color(255/255, 170/255, 60/255)
        self.canvas.setFillColor(yellow)
        self.canvas.rect(0, self.height - 45, self.width, 5, fill=1, stroke=0)

        self.canvas.setFillColor(colors.white)
        text_width = self.canvas.stringWidth("Relatório Meteorológico", "Helvetica-Bold", 25)
        self.add_bold_text("Relatório Meteorológico", ((self.width - text_width) / 2, self.height - 27), font_size=25)
    
        self.canvas.setFillColor(colors.black)
        text_width = self.canvas.stringWidth("Cliente: ", "Helvetica-Bold", 15)
        self.add_bold_text(f"Cliente: ", (30, self.height - 70), font_size=15)
        self.add_text(str(self.user_name).capitalize(), (30 + text_width, self.height - 70), font_size=15)

    def save_pdf_to_file(self, file_path):
        # Save the PDF content to a file.
        self.canvas.save()
        pdf_bytes = self.buffer.getvalue()
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)
        self.buffer.close()
        return pdf_bytes

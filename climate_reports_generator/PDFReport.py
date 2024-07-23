import datetime
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class PDFReport:
    def __init__(self, user_name):
        # Create an in-memory bytes buffer and a canvas with A4 page size
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.user_name = user_name
        self.today_date = datetime.datetime.today().date().strftime("%d/%m/%Y")
        self.add_header()

    def add_text(self, text, position, font_size=12):
        # Add regular text to the canvas
        self.canvas.setFont("Helvetica", font_size)
        self.canvas.drawString(position[0], position[1], text)

    def add_bold_text(self, text, position, font_size=12):
        # Add bold text to the canvas
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
        text_width = self.canvas.stringWidth("Data de confecção: ", "Helvetica-Bold", 15)
        self.add_bold_text(f"Data de confecção: ", (365, self.height - 70), font_size=15)
        self.add_text(self.today_date, (365 + text_width, self.height - 70), font_size=15)

    def add_info(self, title, data:list, start_in_a_new_page=False):
        # Add the info section
        if start_in_a_new_page is True:
            self._add_new_page(title)
        else:
            self.canvas.setFillColor(colors.black)
            self.add_bold_text(title, (30, self.height - 120), font_size=15)
        text_position = (30, 695)
        required_keys = {"data", "fenomeno", "mensagem"}
        for info in data:
            if all(key in info for key in required_keys) is False:
                print("Skipping info section because does not has all required keys")
                continue
            # check if the content can fit in page
            if self._check_if_content_can_fit_in_page(info, text_position) is False:
                self._add_new_page(title)
                text_position = (30, 695)

            is_strong = "forte" in info["mensagem"]
            self._add_phenomenon_title(info["fenomeno"], text_position=text_position, is_strong=is_strong)
            height_position = self._add_phenomenon_info(info, text_position=text_position)
            text_position = (text_position[0], height_position - 20)

    def _add_phenomenon_title(self, phenomenon_name, text_position:tuple, is_strong:bool):
        # Add a rectangle around the phenomenon name
        rect_color = colors.red if is_strong is True else colors.gray
        self.canvas.setFillColor(rect_color)
        self.canvas.rect(text_position[0] - 5, text_position[1] - 5, 130, 20, fill=1, stroke=0)

        self.canvas.setFillColor(colors.white)
        self.add_bold_text(phenomenon_name.capitalize(), (text_position[0], text_position[1]), font_size=13)
        self.canvas.setFillColor(colors.black)

    def _add_phenomenon_info(self, info, text_position:tuple):
        # Add the phenomenon info
        text_width = self.canvas.stringWidth(f'{info["data"]} ', "Helvetica-Bold", 12)
        self.add_bold_text(f'{info["data"]} ', (text_position[0], text_position[1] - 23), font_size=12)
        return self.add_paragraph(info['mensagem'], (text_position[0] + text_width, text_position[1] - 23), font_size=12)


    def add_paragraph(self, text, text_position, font_size=12):
        # Add text paragraphs, respecting margins 
        MARGIN_LEFT = 30
        FIRST_MARGIN_LEFT = text_position[0]
        MARGIN_RIGHT = 30
        LINE_HEIGHT = 14
        self.canvas.setFont("Helvetica", font_size)

        lines = self._get_lines_from_text(text, FIRST_MARGIN_LEFT, MARGIN_LEFT, MARGIN_RIGHT, font_size)

        first_line = True
        # Add lines
        for line in lines:
            current_margin_left = FIRST_MARGIN_LEFT if first_line else MARGIN_LEFT
            self.canvas.drawString(current_margin_left, text_position[1], line)
            text_position = (text_position[0], text_position[1] - LINE_HEIGHT)
            first_line = False 
        return text_position[1]

    def _get_lines_from_text(self, text, first_margin_left, margin_left, margin_right, font_size):
        # Get all lines from the info text
        words = text.split()
        first_line = True
        lines = []
        current_line = ""
        for word in words:
            current_margin_left = first_margin_left if first_line else margin_left

            # Calculate the width of the usable area
            usable_width = self.width - current_margin_left - margin_right

            # Check if adding the next word would exceed the margin
            if self.canvas.stringWidth(current_line + " " + word, "Helvetica", font_size) < usable_width:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
                first_line = False

        # Add the last line
        if current_line:
            lines.append(current_line)
        
        return lines

    def _check_if_content_can_fit_in_page(self, info, position):
        MARGIN_LEFT = 30
        LINE_HEIGHT = 14
        MARGIN_RIGHT = 30
        FONT_SIZE = 12
        text_width = self.canvas.stringWidth(f'{info["data"]} ', "Helvetica-Bold", 12)
        FIRST_MARGIN_LEFT = position[0] + text_width
        
        lines = self._get_lines_from_text(info["mensagem"], FIRST_MARGIN_LEFT, MARGIN_LEFT, MARGIN_RIGHT, FONT_SIZE)
        
        total_lines = len(lines) + 2 # add two to count also the title
        if position[1] - (total_lines * LINE_HEIGHT) <= 50:
            return False
        return True

    def _add_new_page(self, title):
        self.canvas.showPage()
        self.add_header()
        self.canvas.setFillColor(colors.black)
        self.add_bold_text(title, (30, self.height - 120), font_size=15)

    def save_pdf_to_file(self, file_path):
        # Save the PDF content to a file
        self.canvas.save()
        pdf_bytes = self.buffer.getvalue()
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)
        self.buffer.close()
        return pdf_bytes

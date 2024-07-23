import smtplib
from email.message import EmailMessage

from database import Session, User
from datetime import datetime
from env import EMAIL_SENDER, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
from PDFReport import PDFReport


def add_new_user(data):
    try:
        name, email, phone, age = data.split(",")
        new_user = User(name=name, email=email, phone=phone, age=int(age))
        with Session() as session:
            session.add(new_user)
            session.commit()
    except:
        raise Exception("Error: please send the data with the following format: 'name,email,phone,age'")


def validate_phone(phone):
    phones = phone.split(',')
    for num in phones:
        if not num.isdigit():
            raise ValueError(f"Invalid phone number: {num}")
    return phones


def validate_date(date_text):
    try:
        return datetime.strptime(date_text, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValueError(f"Incorrect date format: {date_text}. Should be YYYY-MM-DDTHH:MM")


def send_email(user, report, date):
    # Create a multipart message
    msg = EmailMessage()
    msg['From'] = EMAIL_SENDER
    msg['To'] = user.email
    msg['Subject'] = date.strftime("%Y-%m-%d %H:%M")

    msg.set_content(f"Dear {user.name},\nHere is the climate report from day  {msg['Subject']}.")

    # Attach the PDF
    msg.add_attachment(report, maintype='application', subtype='pdf', filename='report.pdf')


    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent successfully to {user.email}")
    except Exception as e:
        print(f"Failed to send email to {user.email}. Error: {str(e)}")


def get_users_from_db(phones):
    # Search for users with phone and return the existing ones
    with Session() as session:
        users = session.query(User).filter(User.phone.in_(phones)).all()
    
    return users


def generate_pdf_report(content, user, date):
    pdf = PDFReport(user_name=user.name)

    # Add Análise info
    try:
        pdf.add_info(title="Análise", data=content["análise"])
    except KeyError:
        print("The file does not has analysis information")
    # Add Previsao info
    try:
        pdf.add_info(title="Previsão", data=content["previsao"], start_in_a_new_page=True)
    except KeyError:
        print("The file does not has prediction information")

    # Define the file path
    file_path = f"./climate_reports_generator/generated_reports/report_{date}_{user.phone}.pdf"

    # Save the PDF to a file and get the PDF bytes
    pdf_bytes = pdf.save_pdf_to_file(file_path)

    return pdf_bytes



from database import Session, User
from datetime import datetime


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


def send_email(user):
    email = "teste"
    print(f"Sending email with report to {email}")
    pass


def get_users_from_db(phones):
    # Search for users with phone and return the existing ones
    with Session() as session:
        users = session.query(User).filter(User.phone.in_(phones)).all()
    
    return users

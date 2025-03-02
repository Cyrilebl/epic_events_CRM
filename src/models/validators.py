import re
from datetime import datetime


class Validators:
    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    @staticmethod
    def validate_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password)

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = r"^\+\d{2,3} \d{3} \d{3} \d{3}$"
        return re.match(pattern, phone_number)

    @staticmethod
    def validate_date(date):
        try:
            return datetime.strptime(date, "%Y-%m-%d %I:%M %p")
        except ValueError:
            return None

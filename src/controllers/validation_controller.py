from src.models import Validators
from src.views import Prompt, Formatter, ErrorMessage, UserInteraction


class ValidationController:
    def __init__(self):
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.error_message = ErrorMessage()
        self.user_interaction = UserInteraction()

    def get_valid_email(self):
        while True:
            email = self.prompt.input("email")
            if Validators.validate_email(email):
                return email
            self.error_message.invalid_format("email")

    def get_valid_password(self):
        while True:
            password = self.prompt.password(confirm=True)
            if Validators.validate_password(password):
                return password
            self.error_message.invalid_password()

    def get_valid_phone_number(self):
        while True:
            phone_number = self.prompt.input("phone number")
            if Validators.validate_phone_number(phone_number):
                return phone_number
            self.error_message.invalid_phone_number()

    def get_valid_price(self, prompt_text):
        while True:
            price = self.prompt.input(prompt_text)
            try:
                return round(float(price), 2)
            except ValueError:
                self.error_message.invalid_number()

    def get_valid_signature(self):
        while True:
            signature = self.prompt.input("signature (yes/no)").lower()
            if signature == "yes":
                return True
            elif signature == "no":
                return False
            self.error_message.invalid_format("signature")

    def get_valid_date(self, prompt_text):
        while True:
            date_input = self.prompt.datetime_input(prompt_text)
            if Validators.validate_date(date_input):
                return date_input
            self.error_message.invalid_format("date")

    def get_valid_integer(self, prompt_text):
        while True:
            user_input = self.prompt.input(prompt_text)
            try:
                return int(user_input)
            except ValueError:
                self.error_message.invalid_number()

    def get_valid_record(self, session, model, entity_name, action):
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, action)
            record = session.query(model).filter_by(id=record_id).first()
            if record:
                return record
            self.error_message.invalid_id(entity_name)

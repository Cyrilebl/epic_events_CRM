from src.models import User
from src.views import Menu, Prompt, ErrorMessage, SuccessMessage
from .token import Token


class AuthController:
    def __init__(self):
        self.menu = Menu()
        self.prompt = Prompt()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()
        self.token = Token()

    def login(self, session):
        self.menu.login()

        while True:
            email = self.prompt.input("email")
            password = self.prompt.password()

            user = session.query(User).filter_by(email=email).first()

            if not user or not user.check_password(password):
                self.error_message.invalid_credentials()
                continue

            token = self.token.generate_token(user.id, user.role.name)
            return token

    def logout(self):
        self.success_message.confirm_logout()
        return None

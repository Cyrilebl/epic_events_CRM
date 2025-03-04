import os
from src.models import User
from src.views import Prompt, ErrorMessage, SuccessMessage
from .token import Token

TOKEN_FILE = ".auth_token"


def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read()
    return None


class AuthController:
    def __init__(self):
        self.prompt = Prompt()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()
        self.token = Token()

    def login(self, session):
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

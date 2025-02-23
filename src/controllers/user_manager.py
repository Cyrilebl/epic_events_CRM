from .token import Token
from src.models import User, Role
from src.views import Menu, UserPrompt, SuccessMessage, ErrorMessage


class UserManager:
    def __init__(self):
        self.token = Token()
        self.menu = Menu()
        self.user_view = UserPrompt()
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()

    def login(self, session):
        self.menu.login()
        while True:
            email, password = self.user_view.login()

            user = session.query(User).filter_by(email=email).first()

            if not user or not user.check_password(password):
                self.error_message.invalid_credentials()
                continue

            token = self.token.generate_token(user.id, user.role.name)
            return token

    def create_user(self, session):
        first_name, last_name, email, password, role_name = self.user_view.create_user()
        role = session.query(Role).filter_by(name=role_name).first()

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role_name=role.name,
        )
        user.set_password(password)

        session.add(user)
        session.commit()

        self.success_message.confirm_registration(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})"
        )

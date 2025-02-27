from src.models import Role, User
from src.views import ErrorMessage, Formatter, Menu, SuccessMessage, Prompt

from .token import Token


class UserManager:
    def __init__(self):
        self.token = Token()
        self.menu = Menu()
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()

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

    def create_user(self, session):
        last_name = self.prompt.input("last name")
        first_name = self.prompt.input("first name")

        while True:
            email = self.prompt.input("email")
            if User.validate_email(email):
                break
            self.error_message.invalid_email()

        while True:
            password = self.prompt.password(confirm=True)
            if User.validate_password(password):
                break
            self.error_message.invalid_password()

        role_name = self.prompt.role()
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

        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "created",
        )

    def edit_user(self, session, user):
        self.formatter.format_one_user(user)
        while True:
            user_choice = self.prompt.user_choice(5)

            match user_choice:
                case 1:
                    user.last_name = self.prompt.input("new last name")
                case 2:
                    user.first_name = self.prompt.input("new first name")
                case 3:
                    while True:
                        email = self.prompt.input("email")
                        if User.validate_email(email):
                            user.email = email
                            break
                        self.error_message.invalid_email()
                case 4:
                    while True:
                        password = self.prompt.password(confirm=True)
                        if User.validate_password(password):
                            user.set_password(password)
                            break
                        self.error_message.invalid_password()
                case 5:
                    user.role_name = self.prompt.role()
                    continue
            break
        session.commit()

        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "edited",
        )

    def delete_user(self, session, user):
        session.delete(user)
        session.commit()

        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "deleted",
        )

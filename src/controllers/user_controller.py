from src.models import Role, User, DataManager
from src.views import Prompt, ErrorMessage, SuccessMessage

from .token import Token


class UserController:
    def __init__(self):
        self.token = Token()
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()

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

    def create_user(self, session):
        last_name = self.prompt.input("last name")
        first_name = self.prompt.input("first name")

        while True:
            email = self.prompt.input("email")
            if User.validate_email(email):
                break
            self.error_message.invalid_format("email")

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

        self.data_manager.add(session, user)

        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "created",
        )

    def edit_user(self, session, user):
        while True:
            user_choice = self.prompt.user_choice(5)

            match user_choice:
                case 1:
                    self.data_manager.edit_field(
                        session, user, "last_name", self.prompt.input("new last name")
                    )
                case 2:
                    self.data_manager.edit_field(
                        session, user, "first_name", self.prompt.input("new first name")
                    )
                case 3:
                    while True:
                        email = self.prompt.input("email")
                        if User.validate_email(email):
                            self.data_manager.edit_field(session, user, "email", email)
                            break
                        self.error_message.invalid_format("email")
                case 4:
                    while True:
                        password = self.prompt.password(confirm=True)
                        if User.validate_password(password):
                            user.set_password(password)
                            self.data_manager.edit_field(
                                session, user, "password", password
                            )
                            break
                        self.error_message.invalid_password()
                case 5:
                    self.data_manager.edit_field(
                        session, user, "role_name", self.prompt.role()
                    )
                    break
            break

        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "edited",
        )

    def delete_user(self, session, user):
        self.data_manager.delete(session, user)
        self.success_message.confirm_action(
            f"{user.last_name.title()} {user.first_name.title()} ({user.role_name})",
            "deleted",
        )

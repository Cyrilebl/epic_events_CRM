from src.models import Role, User, DataManager
from src.views import Prompt, SuccessMessage
from .validation_controller import ValidationController


class UserController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.success_message = SuccessMessage()
        self.validation = ValidationController()

    def create_user(self, session):
        last_name = self.prompt.input("last name")
        first_name = self.prompt.input("first name")
        email = self.validation.get_valid_email()
        password = self.validation.get_valid_password()
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
                    email = self.validation.get_valid_email()
                    self.data_manager.edit_field(session, user, "email", email)
                case 4:
                    password = self.validation.get_valid_password()
                    user.set_password(password)
                    self.data_manager.edit_field(session, user, "password", password)
                case 5:
                    self.data_manager.edit_field(
                        session, user, "role_name", self.prompt.role()
                    )
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

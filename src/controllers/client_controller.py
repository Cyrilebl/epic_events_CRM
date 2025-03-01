from src.models import User, Client, DataManager
from src.views import Prompt, ErrorMessage, SuccessMessage


class ClientController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()

    def create_client(self, session, user_id):
        last_name = self.prompt.input("last name")
        first_name = self.prompt.input("first name")

        while True:
            email = self.prompt.input("email")
            if Client.validate_email(email):
                break
            self.error_message.invalid_format("email")

        while True:
            phone_number = self.prompt.input("phone number")
            if Client.validate_phone_number(phone_number):
                break
            self.error_message.invalid_phone_number()
        company_name = self.prompt.input("company name")
        information = self.prompt.input("information")
        current_user = session.query(User).filter_by(id=user_id).first()

        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            information=information,
            assigned_commercial=current_user.id,
        )

        self.data_manager.add(session, client)

        self.success_message.confirm_action(
            f"{client.last_name.title()} {client.first_name.title()}",
            "created",
        )

    def edit_client(self, session, client):
        while True:
            user_choice = self.prompt.user_choice(6)

            match user_choice:
                case 1:
                    self.data_manager.edit_field(
                        session, client, "last_name", self.prompt.input("new last name")
                    )
                case 2:
                    self.data_manager.edit_field(
                        session,
                        client,
                        "first_name",
                        self.prompt.input("new last name"),
                    )
                case 3:
                    while True:
                        email = self.prompt.input("email")
                        if Client.validate_email(email):
                            self.data_manager.edit_field(
                                session, client, "email", email
                            )
                            break
                        self.error_message.invalid_format("email")
                case 4:
                    while True:
                        phone_number = self.prompt.input("phone number")
                        if Client.validate_phone_number(phone_number):
                            self.data_manager.edit_field(
                                session, client, "phone_number", phone_number
                            )
                            break
                        self.error_message.invalid_phone_number()
                case 5:
                    self.data_manager.edit_field(
                        session,
                        client,
                        "company_name",
                        self.prompt.input("company name"),
                    )
                case 6:
                    self.data_manager.edit_field(
                        session,
                        client,
                        "information",
                        self.prompt.input("information"),
                    )
                    break
            break

        self.success_message.confirm_action(
            f"{client.last_name.title()} {client.first_name.title()}",
            "edited",
        )

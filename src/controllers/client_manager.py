from src.models import User, Client
from src.views import ErrorMessage, Formatter, SuccessMessage, Prompt


class ClientManager:
    def __init__(self):
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()

    def create_client(self, session, user_id):
        last_name = self.prompt.input("last name")
        first_name = self.prompt.input("first name")

        while True:
            email = self.prompt.input("email")
            if User.validate_email(email):
                break
            self.error_message.invalid_email()

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

        session.add(client)
        session.commit()

        self.success_message.confirm_action(
            f"{client.last_name.title()} {client.first_name.title()}",
            "created",
        )

    def edit_client(self, session, user):
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

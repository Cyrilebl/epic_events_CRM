from src.models import User, Client, Contract, DataManager
from src.views import Prompt, Formatter, ErrorMessage, SuccessMessage, UserInteraction


class ContractController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()
        self.user_interaction = UserInteraction()

    def get_valid_price(self, prompt_text):
        while True:
            price = self.prompt.input(prompt_text)
            try:
                price = float(price)
                price = round(price, 2)
                if Contract.validate_price(price):
                    return price
            except ValueError:
                self.error_message.invalid_number()

    def get_valid_record(self, session, model, entity_name):
        records = session.query(model).all()
        (
            self.formatter.format_clients(records)
            if model == Client
            else self.formatter.format_users(records)
        )
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, "add")
            record = session.query(model).filter_by(id=record_id).first()
            if record:
                return record
            self.error_message.invalid_id(entity_name)

    def create_contract(self, session):
        total_price = self.get_valid_price("total price")
        remaining_balance = self.get_valid_price("remaining balance")
        client = self.get_valid_record(session, Client, "client")
        user = self.get_valid_record(session, User, "user")

        while True:
            signature = self.prompt.input("signature (yes/no)").lower()
            if signature == "yes":
                signature = True
                break
            elif signature == "no":
                signature = False
                break

        contract = Contract(
            total_price=total_price,
            remaining_balance=remaining_balance,
            client_id=client.id,
            assigned_commercial=user.id,
            signature=signature,
        )

        self.data_manager.add(session, contract)

        self.success_message.confirm_action(
            "contract".title(),
            "created",
        )

    def edit_contract(self, session, user):
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
                        if Contract.validate_email(email):
                            self.data_manager.edit_field(session, user, "email", email)
                            break
                        self.error_message.invalid_email()
                case 4:
                    while True:
                        password = self.prompt.password(confirm=True)
                        if Contract.validate_password(password):
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

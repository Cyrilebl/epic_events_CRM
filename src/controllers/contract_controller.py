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
                return round(float(price), 2)
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

    def get_valid_signature(self):
        while True:
            signature = self.prompt.input("signature (yes/no)").lower()
            if signature == "yes":
                return True
            elif signature == "no":
                return False
            self.error_message.invalid_format("signature")

    def create_contract(self, session):
        total_price = self.get_valid_price("total price")
        remaining_balance = self.get_valid_price("remaining balance")
        client = self.get_valid_record(session, Client, "client")
        user = self.get_valid_record(session, User, "user")
        signature = self.get_valid_signature()

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

    def edit_contract(self, session, contract):
        while True:
            user_choice = self.prompt.user_choice(3)

            match user_choice:
                case 1:
                    self.data_manager.edit_field(
                        session,
                        contract,
                        "total_price",
                        self.prompt.input("new total price"),
                    )
                case 2:
                    self.data_manager.edit_field(
                        session,
                        contract,
                        "remaining_balance",
                        self.prompt.input("remaining balance"),
                    )
                case 3:
                    signature = self.get_valid_signature()
                    self.data_manager.edit_field(
                        session, contract, "signature", signature
                    )
                    break
            break

        self.success_message.confirm_action(
            f"Contract '{contract.id}'",
            "edited",
        )

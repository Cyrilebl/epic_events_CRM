from src.models import Client, Contract, DataManager
from src.views import Prompt, Formatter, SuccessMessage
from .validation_controller import ValidationController


class ContractController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.success_message = SuccessMessage()
        self.validation = ValidationController()

    def create_contract(self, session):
        total_price = self.validation.get_valid_price("total price")
        remaining_balance = self.validation.get_valid_price("remaining balance")
        signature = self.validation.get_valid_signature()

        clients = session.query(Client).all()
        display_clients = self.formatter.format_clients(clients)
        if not display_clients:
            return
        client = self.validation.get_valid_record(session, Client, "client", "add")

        contract = Contract(
            total_price=total_price,
            remaining_balance=remaining_balance,
            signature=signature,
            client_id=client.id,
            assigned_commercial=client.assigned_commercial,
        )

        self.data_manager.add(session, contract)

        self.success_message.confirm_action(
            f"Contract nº{contract.id}",
            "created",
        )

    def edit_contract(self, session, contract):
        while True:
            user_choice = self.prompt.user_choice(3)

            match user_choice:
                case 1:
                    total_price = self.validation.get_valid_price("total price")
                    self.data_manager.edit_field(
                        session, contract, "total_price", total_price
                    )
                case 2:
                    remaining_balance = self.validation.get_valid_price(
                        "remaining balance"
                    )
                    self.data_manager.edit_field(
                        session, contract, "remaining_balance", remaining_balance
                    )
                case 3:
                    signature = self.validation.get_valid_signature()
                    self.data_manager.edit_field(
                        session, contract, "signature", signature
                    )
            break

        self.success_message.confirm_action(
            f"Contract nº{contract.id}",
            "edited",
        )

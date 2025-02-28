from .user_controller import UserController
from .client_controller import ClientController
from .contract_controller import ContractController
from .event_controller import EventController
from src.views import Menu, Formatter, SuccessMessage, ErrorMessage, UserInteraction
from src.models import User, Client, Contract, Event


class MenuController:
    def __init__(self):
        self.menu = Menu()
        self.formatter = Formatter()
        self.user_controller = UserController()
        self.client_controller = ClientController()
        self.contract_controller = ContractController()
        self.event_controller = EventController()
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()
        self.user_interaction = UserInteraction()

    def show_menu(self, role):
        match role:
            case "manager":
                return self.menu.manager()
            case "commercial":
                return self.menu.commercial()
            case "support":
                return self.menu.support()

    def get_valid_record(self, session, model, entity_name, action):
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, action)
            record = session.query(model).filter_by(id=record_id).first()
            if record:
                return record
            self.error_message.invalid_id(entity_name)

    def show_data(self, session, user_input):
        match user_input:
            case 1:
                clients_data = session.query(Client).all()
                return self.formatter.format_clients(clients_data)
            case 2:
                contracts_data = session.query(Contract).all()
                return self.formatter.format_contracts(contracts_data)
            case 3:
                events_data = session.query(Event).all()
                return self.formatter.format_events(events_data)

    def user_is_manager(self, session, user_input):
        users_data = session.query(User).all()
        contracts_data = session.query(Contract).all()

        match user_input:
            case 4:
                self.user_controller.create_user(session)

            case 5:
                self.formatter.format_users(users_data)
                user = self.get_valid_record(session, User, "user", "modify")
                self.formatter.format_one_user(user)
                self.user_controller.edit_user(session, user)

            case 6:
                self.formatter.format_users(users_data)
                user = self.get_valid_record(session, User, "user", "delete")
                self.user_controller.delete_user(session)

            case 7:
                self.contract_controller.create_contract(session)

            case 8:
                self.formatter.format_contracts(contracts_data)
                contract = self.get_valid_record(
                    session, Contract, "contract", "modify"
                )
                self.formatter.format_one_contract(contract)
                self.contract_controller.edit_contract(session, contract)

    def user_is_commercial(self, session, user_id, user_input):
        match user_input:
            case 4:
                self.client_controller.create_client(session, user_id)

            case 5:
                clients_assign_to_commercial = (
                    session.query(Client).filter_by(assigned_commercial=user_id).all()
                )
                self.formatter.format_clients(clients_assign_to_commercial)
                client = self.get_valid_record(session, Client, "client", "modify")
                self.formatter.format_one_client(client)
                self.client_controller.edit_client(session, client)

            case 6:
                contracts_assign_to_commercial = (
                    session.query(Contract).filter_by(assigned_commercial=user_id).all()
                )
                self.formatter.format_contracts(contracts_assign_to_commercial)
                contract = self.get_valid_record(
                    session, Contract, "contract", "modify"
                )
                self.formatter.format_one_contract(contract)
                self.contract_controller.edit_contract(session, contract)

            case 7:
                clients_assign_to_commercial = (
                    session.query(Client).filter_by(assigned_commercial=user_id).all()
                )
                self.event_controller.create_event(
                    session, clients_assign_to_commercial
                )

    def user_is_support(self):
        pass

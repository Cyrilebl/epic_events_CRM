from src.views import Menu, Formatter
from src.models import User, Client, Contract, Event
from .user_controller import UserController
from .client_controller import ClientController
from .contract_controller import ContractController
from .event_controller import EventController
from .validation_controller import ValidationController


class MenuController:
    def __init__(self):
        self.menu = Menu()
        self.formatter = Formatter()
        self.user_controller = UserController()
        self.client_controller = ClientController()
        self.contract_controller = ContractController()
        self.event_controller = EventController()
        self.validation = ValidationController()

    def show_menu(self, role):
        match role:
            case "manager":
                return self.menu.manager()
            case "commercial":
                return self.menu.commercial()
            case "support":
                return self.menu.support()

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
                user = self.validation.get_valid_record(session, User, "user", "modify")
                self.formatter.format_one_user(user)
                self.user_controller.edit_user(session, user)

            case 6:
                self.formatter.format_users(users_data)
                user = self.validation.get_valid_record(session, User, "user", "delete")
                self.user_controller.delete_user(session)

            case 7:
                self.contract_controller.create_contract(session)

            case 8:
                self.formatter.format_contracts(contracts_data)
                contract = self.validation.get_valid_record(
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
                client = self.validation.get_valid_record(
                    session, Client, "client", "modify"
                )
                self.formatter.format_one_client(client)
                self.client_controller.edit_client(session, client)

            case 6:
                contracts_assigned_to_commercial = (
                    session.query(Contract).filter_by(assigned_commercial=user_id).all()
                )
                self.formatter.format_contracts(contracts_assigned_to_commercial)
                contract = self.validation.get_valid_record(
                    session, Contract, "contract", "modify"
                )
                self.formatter.format_one_contract(contract)
                self.contract_controller.edit_contract(session, contract)

            case 7:
                self.event_controller.create_event(session, user_id)

    def user_is_support(self, session, user_id, user_input):
        match user_input:
            case 4:
                events_assigned_to_support = (
                    session.query(Event).filter_by(assigned_support=user_id).all()
                )
                display_events = self.formatter.format_events(
                    events_assigned_to_support
                )
                if not display_events:
                    return
                event = self.validation.get_valid_record(
                    session, Event, "event", "modify"
                )
                self.formatter.format_one_event(event)
                self.event_controller.edit_event(session, event)

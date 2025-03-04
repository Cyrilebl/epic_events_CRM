from src.views import Menu, Formatter
from src.models import User, Client, Contract, Event
from .user_controller import UserController
from .client_controller import ClientController
from .contract_controller import ContractController
from .event_controller import EventController
from .utility_controller import UtilityController


class MenuController:
    def __init__(self):
        self.menu = Menu()
        self.formatter = Formatter()
        self.user_controller = UserController()
        self.client_controller = ClientController()
        self.contract_controller = ContractController()
        self.event_controller = EventController()
        self.utility = UtilityController()

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
        match user_input:
            case 4:
                users_data = session.query(User).all()
                self.formatter.format_users(users_data)

            case 5:
                self.user_controller.create_user(session)

            case 6:
                valid_user_ids = self.utility.get_records_by_filter(session, Client)
                user = self.utility.get_valid_record(
                    session, User, "user", "modify", valid_user_ids
                )
                self.formatter.format_one_user(user)
                self.user_controller.edit_user(session, user)

            case 7:
                valid_user_ids = self.utility.get_records_by_filter(session, Client)
                user = self.utility.get_valid_record(
                    session, User, "user", "delete", valid_user_ids
                )
                self.user_controller.delete_user(session)

            case 8:
                self.contract_controller.create_contract(session)

            case 9:
                valid_contract_ids = self.utility.get_records_by_filter(
                    session, Contract
                )
                contract = self.utility.get_valid_record(
                    session, Contract, "contract", "modify", valid_contract_ids
                )
                self.formatter.format_one_contract(contract)
                self.contract_controller.edit_contract(session, contract)

            case 10:
                self.utility.get_records_by_filter(
                    session, Event, assigned_support=None
                )

            case 11:
                self.event_controller.assign_support(session)

    def user_is_commercial(self, session, user_id, user_input):
        match user_input:
            case 4:
                self.client_controller.create_client(session, user_id)

            case 5:
                valid_client_ids = self.utility.get_records_by_filter(
                    session, Client, assigned_commercial=user_id
                )
                client = self.utility.get_valid_record(
                    session, Client, "client", "modify", valid_client_ids
                )

                self.formatter.format_one_client(client)
                self.client_controller.edit_client(session, client)

            case 6:
                self.utility.get_records_by_filter(
                    session, Contract, assigned_commercial=user_id, signature=False
                )

            case 7:
                valid_contract_ids = self.utility.get_records_by_filter(
                    session, Contract, assigned_commercial=user_id
                )
                contract = self.utility.get_valid_record(
                    session, Contract, "contract", "modify", valid_contract_ids
                )
                self.formatter.format_one_contract(contract)
                self.contract_controller.edit_contract(session, contract)

            case 8:
                self.event_controller.create_event(session, user_id)

    def user_is_support(self, session, user_id, user_input):
        match user_input:
            case 4:
                self.utility.get_records_by_filter(
                    session, Event, assigned_support=user_id
                )

            case 5:
                valid_event_ids = self.utility.get_records_by_filter(
                    session, Event, assigned_support=user_id
                )
                event = self.utility.get_valid_record(
                    session, Event, "event", "modify", valid_event_ids
                )
                self.formatter.format_one_event(event)
                self.event_controller.edit_event(session, event)

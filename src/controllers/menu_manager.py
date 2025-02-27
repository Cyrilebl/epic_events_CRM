from .user_manager import UserManager
from .client_manager import ClientManager
from src.views import Menu, Formatter, ErrorMessage, UserInteraction
from src.models import User, Client, Contract, Event


class MenuManager:
    def __init__(self):
        self.menu = Menu()
        self.formatter = Formatter()
        self.user_manager = UserManager()
        self.client_manager = ClientManager()
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
        match user_input:
            case 4:
                self.user_manager.create_user(session)
            case 5:
                self.formatter.format_users(users_data)
                while True:
                    user_id = self.user_interaction.prompt_user_selection(
                        "user", "modify"
                    )
                    user = session.query(User).filter_by(id=user_id).first()
                    if user:
                        break
                    self.error_message.invalid_id("user")
                self.user_manager.edit_user(session, user)
            case 6:
                self.formatter.format_users(users_data)
                while True:
                    user_id = self.user_interaction.prompt_user_selection(
                        "user", "delete"
                    )
                    user = session.query(User).filter_by(id=user_id).first()
                    if user:
                        break
                    self.error_message.invalid_id("user")
                self.user_manager.delete_user(session, user)

    def user_is_commercial(self, session, user_id, user_input):
        match user_input:
            case 4:
                self.client_manager.create_client(session, user_id)
            case 5:
                pass

    def user_is_support(self):
        pass

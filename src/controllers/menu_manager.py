from src.views import Menu, Formatter
from src.models import Client, Contract, Event


class MenuManager:
    def __init__(self):
        self.menu = Menu()
        self.formatter = Formatter()

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
                return self.formatter.format_contract(contracts_data)

            case 3:
                events_data = session.query(Event).all()
                return self.formatter.format_event(events_data)

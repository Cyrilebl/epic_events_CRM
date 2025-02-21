from src.views.menu import Menu


class MenuManager:
    def __init__(self):
        self.menu = Menu()

    def show_menu(self, role):
        match role:
            case "manager":
                return self.menu.manager()
            case "commercial":
                return self.menu.commercial()
            case "support":
                return self.menu.support()

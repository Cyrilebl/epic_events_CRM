from .token import Token
from .user_controller import UserController
from .menu_controller import MenuController
from src.models import init_db
from src.views import Menu, UserInteraction


class MainController:
    def __init__(self):
        self.token = Token()
        self.user_controller = UserController()
        self.menu_controller = MenuController()
        self.session = init_db()
        self.menu = Menu()
        self.user_interaction = UserInteraction()

    def run(self):
        # Login
        self.menu.login()
        token = self.user_controller.login(self.session)
        user_id, role = self.token.verify_token(token)

        # Menu
        while True:
            user_input = self.menu_controller.show_menu(role)

            # Logout
            if user_input == "logout":
                self.user_controller.logout()
                break

            self.menu_controller.show_data(self.session, user_input)

            match role:
                case "manager":
                    self.menu_controller.user_is_manager(self.session, user_input)
                case "commercial":
                    self.menu_controller.user_is_commercial(
                        self.session, user_id, user_input
                    )
                case "support":
                    self.menu_controller.user_is_support(
                        self.session, user_id, user_input
                    )

            self.user_interaction.return_to_menu()

        # user = "test"
        # if user.has_permission("assign_support"):
        #     events_without_assigned_support = (
        #         self.session.query(Event).filter(Event.assigned_support.is_(None)).all()
        #     )

        # if user.has_permission("edit_contracts_as_commercial"):
        #     unsigned_contracts = (
        #         self.session.query(Contract).filter(Contract.signature.is_(False)).all()
        #     )

        # if user.has_permission("edit_events_as_support"):
        #     unpaid_contracts = (
        #         self.session.query(Contract)
        #         .filter(Contract.remaining_balance > 0)
        #         .all()
        #     )

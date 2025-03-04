from src.models import init_db
from src.views import Menu, UserInteraction
from .token import Token
from .auth_controller import AuthController
from .menu_controller import MenuController
from src.utils import ReturnToMainMenu


class MainController:
    def __init__(self):
        self.session = init_db()
        self.menu = Menu()
        self.user_interaction = UserInteraction()
        self.token = Token()
        self.auth = AuthController()
        self.menu_controller = MenuController()

    def run(self):
        # Login
        self.menu.login()
        token = self.auth.login(self.session)
        user_id, role = self.token.verify_token(token)

        # Menu
        while True:
            user_input = self.menu_controller.show_menu(role)

            # Logout
            if user_input == "logout":
                self.auth.logout()
                break

            try:
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
            except ReturnToMainMenu:
                pass

            self.user_interaction.return_to_menu()

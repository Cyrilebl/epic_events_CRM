from src.models import init_db
from src.views import UserInteraction
from .token import Token
from .auth_controller import AuthController
from .menu_controller import MenuController
from src.utils import ReturnToMainMenu

import os
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
    auto_session_tracking=True,
)


class MainController:
    def __init__(self):
        self.session = init_db()
        self.user_interaction = UserInteraction()
        self.token = Token()
        self.auth = AuthController()
        self.menu = MenuController()

    def run(self):
        # Login
        token = self.auth.login(self.session)
        if not token:
            exit()
        user_id, role = self.token.verify_token(token)

        while True:
            user_input = self.menu.show_menu(role)

            # Verify token before allowing any action
            user_id, role = self.token.verify_token(token)
            if user_id is None:
                break

            # Logout
            if user_input == "logout":
                self.auth.logout()
                break

            try:
                self.menu.show_data(self.session, user_input)

                match role:
                    case "manager":
                        self.menu.user_is_manager(self.session, user_input)
                    case "commercial":
                        self.menu.user_is_commercial(self.session, user_id, user_input)
                    case "support":
                        self.menu.user_is_support(self.session, user_id, user_input)

            except ReturnToMainMenu:
                pass

            self.user_interaction.return_to_menu()

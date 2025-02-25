from .user_manager import UserManager
from .menu_manager import MenuManager
from .token import Token
from src.models import init_db
from src.views import SuccessMessage, UserInteraction


class MainController:
    def __init__(self):
        self.session = init_db()
        self.manager = UserManager()
        self.menu_manager = MenuManager()
        self.token = Token()
        self.success_message = SuccessMessage()
        self.user_interaction = UserInteraction()

    def run(self):
        # Login
        token = self.manager.login(self.session)
        user_id, role = self.token.verify_token(token)

        # Menu
        # if not user:
        #     return "Access denied. Please log in."
        # else
        while True:
            user_input = self.menu_manager.show_menu(role)
            self.menu_manager.show_data(self.session, user_input)
            self.menu_manager.user_is_manager(self.session, user_input)
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

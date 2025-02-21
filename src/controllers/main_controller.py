from .user_manager import UserManager
from .create_role import create_role
from .menu_manager import MenuManager
from .token import Token
from src.models.database import init_db


class MainController:
    def __init__(self):
        self.session = init_db()
        self.manager = UserManager()
        self.menu_manager = MenuManager()
        self.token = Token()

    def run(self):
        create_role(self.session)

        self.manager.create_user(self.session)
        token = self.manager.login(self.session)
        user_id, role = self.token.verify_token(token)
        self.menu_manager.show_menu(role)

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

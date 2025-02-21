from .user_choice import user_choice


class Menu:
    def login(self):
        title = "EPIC EVENTS CRM"
        print("-" * 40)
        print(title.center(40))
        print("-" * 40)
        print(
            """

          ------ Login ------
    """
        )

    def menu_header(self):
        title = "MENU"
        print("-" * 40)
        print(title.center(40))
        print("-" * 40)

    def common_menu(self):
        print(
            """
[1] Clients
[2] Contracts
[3] Events"""
        )

    def manager(self):
        self.menu_header()
        self.common_menu()
        print(
            """
User Management:
[4] Create user
[5] Update user
[6] Delete user

Contract Management:
[7] Create contract
[8] Update contract
[9] Assign support agent to contract
    """
        )
        return user_choice(9)

    def commercial(self):
        self.menu_header()
        self.common_menu()
        print(
            """
Client Management:
[4] Create client
[5] Update client

Contract Management:
[6] Update contract

Event Management:
[7] Create event
        """
        )
        return user_choice(7)

    def support(self):
        self.menu_header()
        self.common_menu()
        print(
            """
Event Management:
[4] Update event"""
        )
        return user_choice(4)

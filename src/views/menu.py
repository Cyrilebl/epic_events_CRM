import click

from .prompt import Prompt


class Menu:
    def __init__(self):
        self.prompt = Prompt()

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

    def header(self):
        title = "MENU"
        print("-" * 40)
        print(title.center(40))
        print("-" * 40)

    def logout(self):
        print("[0] Logout")

    def read_menu(self):
        print(
            f"""
{click.style("Read Data", fg="cyan")}
[1] Read clients
[2] Read contracts
[3] Read events"""
        )

    def manager(self):
        self.header()
        self.read_menu()
        print(
            f"""
{click.style("User Management", fg="cyan")}
[4] Create user
[5] Update user
[6] Delete user

{click.style("Contract Management", fg="cyan")}
[7] Create contract
[8] Update contract

{click.style("Event Management", fg="cyan")}
[9] Assign support agent to event
    """
        )
        self.logout()
        return self.prompt.user_choice(9)

    def commercial(self):
        self.header()
        self.read_menu()
        print(
            f"""
{click.style("Client Management", fg="cyan")}
[4] Create client
[5] Update client

{click.style("Contract Management", fg="cyan")}
[6] Update contract

{click.style("Event Management", fg="cyan")}
[7] Create event
        """
        )
        self.logout()
        return self.prompt.user_choice(7)

    def support(self):
        self.header()
        self.read_menu()
        print(
            f"""
{click.style("Event Management", fg="cyan")}
[4] Update event"""
        )
        self.logout()
        return self.prompt.user_choice(4)

import click

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

    def read_menu(self):
        print(
            f"""
{click.style("Read Data", fg="cyan")}
[1] Read clients
[2] Read contracts
[3] Read events"""
        )

    def manager(self):
        self.menu_header()
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
[9] Assign support agent to contract

{click.style("Event Management", fg="cyan")}
[10] Update event
    """
        )
        return user_choice(10)

    def commercial(self):
        self.menu_header()
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
        return user_choice(7)

    def support(self):
        self.menu_header()
        self.read_menu()
        print(
            f"""
{click.style("Event Management", fg="cyan")}
[4] Update event"""
        )
        return user_choice(4)

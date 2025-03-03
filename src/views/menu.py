import click

from .prompt import Prompt


class Menu:
    def __init__(self):
        self.prompt = Prompt()

    def login(self):
        title = "EPIC EVENTS CRM"
        line = click.style("-" * 40)

        click.echo(line)
        click.echo(title.center(40))
        click.echo(line)
        click.echo("")
        click.echo("------ Login ------".center(40))
        click.echo("")

    def header(self):
        title = "MENU"
        line = click.style("-" * 40)

        click.echo(line)
        click.echo(title.center(40))
        click.echo(line)

    def section_title(self, icon, title):
        return click.style(f"{icon} {title}", fg="cyan")

    def logout(self):
        click.echo(click.style("🚪 [0] Logout", fg="red"))

    def read_menu(self):
        print(
            f"""
{self.section_title("📖", "Read Data")}
[1] View clients
[2] View contracts
[3] View events"""
        )

    def manager(self):
        self.header()
        self.read_menu()
        print(
            f"""
{self.section_title("👤", "User Management")}
[4] Create user
[5] Update user
[6] Delete user

{self.section_title("📜", "Contract Management")}
[7] Create contract
[8] Update contract

{self.section_title("🎟️ ", "Event Management")}
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
{self.section_title("👤", "Client Management")}
[4] Create client
[5] Update client

{self.section_title("📜", "Contract Management")}
[6] Update contract
 
{self.section_title("🎟️ ", "Event Management")}
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
{self.section_title("🎟️ ", "Event Management")}
[4] Update event
        """
        )
        self.logout()
        return self.prompt.user_choice(4)

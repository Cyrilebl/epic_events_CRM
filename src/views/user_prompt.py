import re
import click


class UserPrompt:
    def validate_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    def prompt_email(self):
        while True:
            email = click.prompt("Email").strip()
            if self.validate_email(email):
                return email
            click.echo(click.style("Invalid email format. Please try again."), fg="red")

    def login(self):
        email = self.prompt_email()
        password = click.prompt("Password: ", hide_input=True)
        return email, password

    def create_user(self):
        first_name = click.prompt("First name")
        last_name = click.prompt("Last name")
        email = self.prompt_email()
        password = click.prompt("Password: ", hide_input=True, confirmation_prompt=True)
        role_name = click.prompt(
            "User role",
            type=click.Choice(
                ["manager", "commercial", "support"], case_sensitive=False
            ),
        )

        return first_name, last_name, email, password, role_name

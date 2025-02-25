import re
import click


class UserPrompt:
    def validate_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    def prompt_email(self):
        while True:
            email = click.prompt(click.style("Email", fg="blue", bold=True))
            if self.validate_email(email):
                return email
            click.echo(
                click.style(
                    "Invalid email format. Please try again.", fg="red", bold=True
                )
            )

    def login(self):
        email = self.prompt_email()
        password = click.prompt(
            click.style("Password", fg="blue", bold=True), hide_input=True
        )
        return email, password

    def create_user(self):
        first_name = click.prompt(click.style("First name", fg="blue", bold=True))
        last_name = click.prompt(click.style("Last name", fg="blue", bold=True))
        email = self.prompt_email()
        password = click.prompt(
            click.style("Password", fg="blue", bold=True),
            hide_input=True,
            confirmation_prompt=True,
        )
        role_name = click.prompt(
            click.style("User role", fg="blue", bold=True),
            type=click.Choice(
                ["manager", "commercial", "support"], case_sensitive=False
            ),
        )

        return first_name, last_name, email, password, role_name

    def edit_user(self, user):
        while True:
            user_input = click.prompt(
                click.style(
                    "Enter the number of the field to modify (1-5)",
                    fg="magenta",
                    bold=True,
                ),
                type=int,
            )

            match user_input:
                case 1:
                    user.last_name = click.prompt(
                        click.style("New Last Name", fg="blue", bold=True)
                    )
                case 2:
                    user.first_name = click.prompt(
                        click.style("New First Name", fg="blue", bold=True)
                    )
                case 3:
                    user.email = click.prompt(
                        click.style("New Email", fg="blue", bold=True)
                    )
                case 4:
                    user.password_hash = click.prompt(
                        click.style(
                            "Password",
                            hide_input=True,
                            confirmation_prompt=True,
                            fg="blue",
                            bold=True,
                        )
                    )
                case 5:
                    user.role_name = click.prompt(
                        click.style("New Role", fg="blue", bold=True)
                    )
                case _:
                    click.echo(
                        click.style(
                            "Invalid choice. Please enter a number between 1 and 5.",
                            fg="red",
                            bold=True,
                        ),
                        err=True,
                    )
                    continue
            break

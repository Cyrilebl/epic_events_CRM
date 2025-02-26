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

    def validate_password(self, password):
        pattern = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password)

    def prompt_password(self):
        while True:
            password = click.prompt(
                click.style("Password", fg="blue", bold=True),
                hide_input=True,
                confirmation_prompt=True,
            )
            if self.validate_password(password):
                return password
            click.echo(
                click.style(
                    "Invalid password format. Must have at least one uppercase letter, one digit, and be at least 8 characters long.",
                    fg="red",
                    bold=True,
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
        password = self.prompt_password()
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
                    user.email = self.prompt_email()
                case 4:
                    new_password = self.prompt_password()
                    user.set_password(new_password)
                case 5:
                    user.role_name = click.prompt(
                        click.style("New role", fg="blue", bold=True),
                        type=click.Choice(
                            ["manager", "commercial", "support"], case_sensitive=False
                        ),
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

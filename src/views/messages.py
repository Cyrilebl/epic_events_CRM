import click


class ErrorMessage:
    def invalid_credentials(self):
        click.echo(click.style("Invalid credentials.", fg="red", bold=True))

    def token_expired(self):
        click.echo(
            click.style("Token expired, please log in again.", fg="red", bold=True)
        )

    def invalid_token(self):
        click.echo(click.style("Invalid token.", fg="red", bold=True))

    def invalid_id(self, name):
        click.echo(
            click.style(
                f"{name.title()} not found. Please enter a valid ID.",
                fg="red",
                bold=True,
            )
        )

    def invalid_format(self, name):
        click.echo(
            click.style(
                f"Invalid {name} format. Please try again.", fg="red", bold=True
            )
        )

    def invalid_password(self):
        click.echo(
            click.style(
                "Invalid password format. Must have at least one uppercase letter, one digit, and be at least 8 characters long.",
                fg="red",
                bold=True,
            )
        )

    def invalid_phone_number(self):
        click.echo(
            click.style(
                "Invalid phone number format. Use: +XX XXX XXX XXX or +XXX XXX XXX XXX.",
                fg="red",
                bold=True,
            )
        )

    def invalid_number(self):
        click.echo(
            click.style(
                "Invalid input. Please enter a number.",
                fg="red",
                bold=True,
            )
        )


class SuccessMessage:
    def confirm_action(self, name, action):
        click.echo(
            click.style(
                f"{name} has been successfully {action}.", fg="green", bold=True
            )
        )

    def confirm_logout(self):
        click.echo(
            click.style("You have been logged out successfully.", fg="green", bold=True)
        )


class UserInteraction:
    def return_to_menu(self):
        click.pause()

    def prompt_user_selection(self, name, action):
        return click.prompt(
            click.style(
                f"Enter the {name} ID you want to {action}",
                fg="magenta",
                bold="True",
            ),
            type=int,
        )

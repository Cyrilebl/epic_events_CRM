import click


class ErrorMessage:
    def invalid_credentials(self):
        click.echo(
            click.style("Invalid credentials, please try again.", fg="red", bold=True)
        )

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


class SuccessMessage:
    def confirm_action(self, name, action):
        click.echo(
            click.style(
                f"{name} has been successfully {action}.", fg="green", bold=True
            )
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

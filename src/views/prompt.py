import click


class Prompt:
    def input(self, label):
        """Prompt user for a general input field."""
        return click.prompt(click.style(label.title(), fg="blue", bold=True))

    def password(self, confirm=False):
        return click.prompt(
            click.style("Password", fg="blue", bold=True),
            hide_input=True,
            confirmation_prompt=confirm,
        )

    def role(self):
        return click.prompt(
            click.style("Role", fg="blue", bold=True),
            type=click.Choice(
                ["manager", "commercial", "support"], case_sensitive=False
            ),
        )

    def datetime_input(self, label):
        return click.prompt(click.style(label, fg="blue", bold=True))

    def user_choice(self, number_of_choices):
        while True:
            try:
                user_choice = int(
                    click.prompt(
                        click.style("Enter your choice", fg="magenta", bold=True)
                    )
                )

                if user_choice == 0:
                    return "logout"
                elif 0 < user_choice <= number_of_choices:
                    return user_choice
                else:
                    click.echo(click.style("Invalid choice.", fg="red", bold=True))
            except ValueError:
                click.echo(
                    click.style(
                        "Invalid input. Please enter a number.", fg="red", bold=True
                    )
                )

    def try_again_yes_or_no(self):
        while True:
            user_choice = click.prompt(
                click.style(
                    "Do you want to try again ? (yes/no)", fg="magenta", bold=True
                )
            ).lower()

            if user_choice == "yes":
                return True
            elif user_choice == "no":
                click.echo(
                    click.style("Thanks for visiting us !", fg="green", bold=True)
                )
                return False
            else:
                click.echo(
                    click.style("Please enter 'yes' or 'no'.", fg="red", bold=True)
                )

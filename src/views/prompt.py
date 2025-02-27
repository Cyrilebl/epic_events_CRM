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

    def user_choice(self, number_of_choices):
        while True:
            try:
                user_choice = int(
                    click.prompt(
                        click.style("Enter your choice", fg="magenta", bold=True)
                    )
                )
                if 0 < user_choice <= number_of_choices:
                    return user_choice
                else:
                    click.echo(click.style("Invalid choice.", fg="red", bold=True))
            except ValueError:
                click.echo(
                    click.style(
                        "Invalid input. Please enter a number.", fg="red", bold=True
                    )
                )

import click


def user_choice(number_of_choices):
    while True:
        try:
            user_choice = int(
                click.prompt(click.style("Enter your choice", fg="magenta", bold=True))
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

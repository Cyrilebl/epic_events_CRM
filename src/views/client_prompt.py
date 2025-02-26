import click


class ClientPrompt:
    def create_user(self):
        first_name = click.prompt(click.style("First name", fg="blue", bold=True))
        last_name = click.prompt(click.style("Last name", fg="blue", bold=True))
        email = self.prompt_email()
        password = self.prompt_password()
        phone_number = ""
        company_name = ""
        information = ""
        creation_date = ""
        last_update_date = ""
        assigned_commercial = ""  # ForeignKey("users.id"))

        return (
            first_name,
            last_name,
            email,
            password,
            phone_number,
            company_name,
            information,
            creation_date,
            last_update_date,
            assigned_commercial,
        )

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

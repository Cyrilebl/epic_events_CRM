import click

from src.models import init_db, Role, User


@click.group()
def cli():
    pass


@click.command()
def create_role():
    session = init_db()

    roles = ["manager", "commercial", "support"]
    created_roles = []
    for role in roles:
        if not session.query(Role).filter(Role.name == role).first():
            session.add(Role(name=role))
            created_roles.append(role)

    session.commit()
    session.close()
    if created_roles:
        click.echo(f"Roles created successfully: {', '.join(created_roles)}.")
    else:
        click.echo("All roles already exist. No changes made.")


@click.command()
@click.option("--first_name", prompt="First name", default="admin")
@click.option("--last_name", prompt="Last name", default="admin")
@click.option("--email", prompt="Email")
@click.option(
    "--password", prompt="Password", hide_input=True, confirmation_prompt=True
)
def create_superuser(first_name, last_name, password, email):
    session = init_db()

    if session.query(User).filter_by(email=email).first():
        click.echo("A superuser with this email already exists.")
        session.close()
        return

    manager_role = session.query(Role).filter_by(name="manager").first()
    if not manager_role:
        click.echo("Error: 'manager' role does not exist. Run 'create-role' first.")
        session.close()
        return

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=manager_role,
    )
    user.set_password(password)

    session.add(user)
    session.commit()
    session.close()
    click.echo("Superuser created successfully.")


cli.add_command(create_role)
cli.add_command(create_superuser)

if __name__ == "__main__":
    cli()

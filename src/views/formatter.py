import click
from tabulate import tabulate


class Formatter:
    def format_one_user(self, user):
        headers = [
            "1. Last name",
            "2. First name",
            "3. Email",
            "4. Password",
            "5. Role",
        ]

        rows = [
            [
                user.last_name,
                user.first_name,
                user.email,
                "xxxxxxxx",
                user.role_name,
            ]
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_users(self, users_data):
        headers = ["ID", "Last name", "First name", "Email", "Role"]

        sorted_users = sorted(users_data, key=lambda user: user.id)
        rows = [
            [
                user.id,
                user.last_name,
                user.first_name,
                user.email,
                user.role_name,
            ]
            for user in sorted_users
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_one_client(self, client):
        headers = [
            "1. Last name",
            "2. First name",
            "3. Email",
            "4. Phone number",
            "5. Company",
            "6. Information",
        ]

        rows = [
            [
                client.last_name,
                client.first_name,
                client.email,
                client.phone_number,
                client.company_name,
                client.information,
            ]
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_clients(self, clients_data):
        if not clients_data:
            click.echo(click.style("No current clients.", fg="yellow", bold=True))
            return

        headers = [
            "ID",
            "Last name",
            "First name",
            "Email",
            "Phone number",
            "Company",
            "Information",
            "Creation date",
            "Last update date",
            "Assigned commercial",
        ]

        sorted_clients = sorted(clients_data, key=lambda client: client.last_name)
        rows = [
            [
                client.id,
                client.last_name,
                client.first_name,
                client.email,
                client.phone_number,
                client.company_name,
                client.information,
                client.creation_date,
                client.last_update_date,
                f"{client.commercial.last_name} {client.commercial.first_name}",
            ]
            for client in sorted_clients
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_one_contract(self, contract):
        headers = [
            "1. Total price",
            "2. Remaining balance",
            "3. Signature",
        ]

        rows = [
            [
                contract.total_price,
                contract.remaining_balance,
                contract.signature,
            ]
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_contracts(self, contracts_data):
        if not contracts_data:
            click.echo(click.style("No contracts available.", fg="yellow", bold=True))
            return

        headers = [
            "ID",
            "Client",
            "Total price",
            "Remaining balance",
            "Creation date",
            "Signature",
            "Assigned commercial",
        ]

        sorted_contracts = sorted(contracts_data, key=lambda contract: contract.id)
        rows = [
            [
                contract.id,
                f"{contract.client.last_name} {contract.client.first_name}",
                contract.total_price,
                contract.remaining_balance,
                contract.creation_date,
                contract.signature,
                f"{contract.client.commercial.last_name} {contract.client.commercial.first_name}",
            ]
            for contract in sorted_contracts
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_one_event(self, event):
        headers = [
            "1. Start date",
            "2. End date",
            "3. Street number",
            "4. Street name",
            "5. Postal code",
            "6. City",
            "7. Country",
            "8. Attendees",
            "9. Notes",
        ]

        rows = [
            [
                event.start_date,
                event.end_date,
                event.street_number,
                event.street_name,
                event.postal_code,
                event.city,
                event.country,
                event.attendees,
                event.notes,
            ]
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

    def format_events(self, events_data):
        if not events_data:
            click.echo(click.style("No events scheduled.", fg="yellow", bold=True))
            return

        headers = [
            "Event ID",
            "Contract ID",
            "Client name",
            "Client contact",
            "Start date",
            "End date",
            "Location",
            "Attendees",
            "Notes",
            "Assigned support",
        ]

        sorted_events = sorted(events_data, key=lambda event: event.id)
        rows = [
            [
                event.id,
                event.contract_id,
                f"{event.contract.client.last_name} {event.contract.client.first_name}",
                f"{event.contract.client.email}/{event.contract.client.phone_number}",
                event.start_date,
                event.end_date,
                f"{event.street_number} {event.street_name}, {event.postal_code} {event.city}, {event.country}",
                event.attendees,
                event.notes,
                (
                    f"{event.support.last_name} {event.support.first_name}"
                    if event.assigned_support
                    else None
                ),
            ]
            for event in sorted_events
        ]

        click.echo(tabulate(rows, headers, tablefmt="grid"))

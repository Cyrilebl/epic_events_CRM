from src.models import Client, Contract, Event, DataManager
from src.views import Prompt, Formatter, SuccessMessage
from .validation_controller import ValidationController


class EventController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.success_message = SuccessMessage()
        self.validation = ValidationController()

    def create_event(self, session, user_id):
        start_date = self.validation.get_valid_date(
            "start date (YYYY-MM-DD HH:MM AM/PM)"
        )
        end_date = self.validation.get_valid_date("end date (YYYY-MM-DD HH:MM AM/PM)")
        street_number = self.prompt.input("street number")
        street_name = self.prompt.input("street name")
        postal_code = self.prompt.input("postal code")
        city = self.prompt.input("city")
        country = self.prompt.input("country")
        attendees = self.validation.get_valid_integer("number of attendees")
        notes = self.prompt.input("notes")

        clients_assigned_to_commercial = (
            session.query(Client).filter_by(assigned_commercial=user_id).all()
        )
        display_clients = self.formatter.format_clients(clients_assigned_to_commercial)
        if not display_clients:
            return

        client = self.validation.get_valid_record(session, Client, "client", "add")

        contracts = (
            session.query(Contract)
            .filter(
                Contract.client_id == client.id,
                Contract.signature == True,
            )
            .all()
        )
        display_contracts = self.formatter.format_contracts(contracts)
        if not display_contracts:
            return

        contract = self.validation.get_valid_record(
            session, Contract, "contract", "add"
        )

        event = Event(
            start_date=start_date,
            end_date=end_date,
            street_number=street_number,
            street_name=street_name,
            postal_code=postal_code,
            city=city,
            country=country,
            attendees=attendees,
            notes=notes,
            client_id=client.id,
            contract_id=contract.id,
        )

        self.data_manager.add(session, event)

        self.success_message.confirm_action(
            f"Event nº{event.id}",
            "created",
        )

    def edit_event(self, session, event):
        while True:
            user_choice = self.prompt.user_choice(3)

            match user_choice:
                case 1:
                    start_date = self.validation.get_valid_date(
                        "new start date (YYYY-MM-DD HH:MM AM/PM)"
                    )
                    self.data_manager.edit_field(
                        session, event, "start_date", start_date
                    )
                case 2:
                    end_date = self.validation.get_valid_date(
                        "new end date (YYYY-MM-DD HH:MM AM/PM)"
                    )
                    self.data_manager.edit_field(session, event, "end_date", end_date)
                case 3:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "street_number",
                        self.prompt.input("street number"),
                    )
                case 4:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "street_name",
                        self.prompt.input("street name"),
                    )
                case 5:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "postal_code",
                        self.prompt.input("postal code"),
                    )
                case 6:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "city",
                        self.prompt.input("city"),
                    )
                case 7:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "country",
                        self.prompt.input("country"),
                    )
                case 8:
                    attendees = self.validation.get_valid_integer("number of attendees")
                    self.data_manager.edit_field(session, event, "attendees", attendees)
                case 9:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "notes",
                        self.prompt.input("notes"),
                    )
            break

        self.success_message.confirm_action(
            f"Event nº{event.id}",
            "edited",
        )

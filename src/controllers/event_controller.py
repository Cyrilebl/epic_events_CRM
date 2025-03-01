from src.models import Client, Contract, Event, DataManager
from src.views import Prompt, Formatter, ErrorMessage, SuccessMessage, UserInteraction


class EventController:
    def __init__(self):
        self.data_manager = DataManager()
        self.prompt = Prompt()
        self.formatter = Formatter()
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()
        self.user_interaction = UserInteraction()

    def get_valid_record(self, session, model, entity_name):
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, "add")
            record = session.query(model).filter_by(id=record_id).first()
            if record:
                return record
            self.error_message.invalid_id(entity_name)

    def get_valid_date(self, prompt_text):
        while True:
            date_input = self.prompt.datetime_input(prompt_text)
            if Event.validate_date(date_input):
                return date_input
            self.error_message.invalid_format("date")

    def get_valid_integer(self, prompt_text):
        while True:
            user_input = self.prompt.input(prompt_text)
            try:
                return int(user_input)
            except ValueError:
                self.error_message.invalid_number()

    def create_event(self, session, clients_assigned_to_commercial):
        start_date = self.get_valid_date("start date (YYYY-MM-DD HH:MM AM/PM)")
        end_date = self.get_valid_date("end date (YYYY-MM-DD HH:MM AM/PM)")
        street_number = self.prompt.input("street number")
        street_name = self.prompt.input("street name")
        postal_code = self.prompt.input("postal code")
        city = self.prompt.input("city")
        country = self.prompt.input("country")
        attendees = self.get_valid_integer("number of attendees")
        notes = self.prompt.input("notes")

        display_clients = self.formatter.format_clients(clients_assigned_to_commercial)
        if not display_clients:
            return

        client = self.get_valid_record(session, Client, "client")

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
            return self.error_message.no_signed_contract()

        contract = self.get_valid_record(session, Contract, "contract")

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
            "event".title(),
            "created",
        )

    def edit_event(self, session, event):
        while True:
            user_choice = self.prompt.user_choice(3)

            match user_choice:
                case 1:
                    start_date = self.get_valid_date(
                        "new start date (YYYY-MM-DD HH:MM AM/PM)"
                    )
                    self.data_manager.edit_field(
                        session,
                        event,
                        "start_date",
                        self.prompt.datetime_input(start_date),
                    )
                case 2:
                    end_date = self.get_valid_date(
                        "new end date (YYYY-MM-DD HH:MM AM/PM)"
                    )
                    self.data_manager.edit_field(
                        session,
                        event,
                        "end_date",
                        self.prompt.datetime_input(end_date),
                    )
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
                    self.data_manager.edit_field(
                        session,
                        event,
                        "attendees",
                        self.prompt.input("number of attendees"),
                    )
                case 9:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "notes",
                        self.prompt.input("notes"),
                    )
            break

        self.success_message.confirm_action(
            f"Event '{event.id}'",
            "edited",
        )

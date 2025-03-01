from src.models import User, Client, Contract, Event, DataManager
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
        records = session.query(model).all()
        (
            self.formatter.format_clients(records)
            if model == Client
            else self.formatter.format_users(records)
        )
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, "add")
            record = session.query(model).filter_by(id=record_id).first()
            if record:
                return record
            self.error_message.invalid_id(entity_name)

    def get_valid_date(self, prompt_text):
        while True:
            date_input = self.prompt.input(prompt_text)
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

    def create_event(self, session):
        start_date = self.get_valid_date("start date (yyyy-mm-dd)")
        end_date = self.get_valid_date("end date (yyyy-mm-dd)")
        street_number = self.prompt.input("street number")
        street_name = self.prompt.input("street name")
        postal_code = self.prompt.input("postal code")
        city = self.prompt.input("city")
        country = self.prompt.input("country")
        attendees = self.get_valid_integer("number of attendees")
        notes = self.prompt.input("notes")
        client = self.get_valid_record(session, Client, "client")
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
        # Un des clients de l'user et signé else No clients with sign contract
        # Afficher les contracts de cet utilisateur else This client doesn't have any contract
        self.data_manager.add(session, event)

        self.success_message.confirm_action(
            "event".title(),
            "created",
        )

    def edit_contract(self, session, event):
        while True:
            user_choice = self.prompt.user_choice(3)

            match user_choice:
                case 1:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "total_price",
                        self.prompt.input("new total price"),
                    )
                case 2:
                    self.data_manager.edit_field(
                        session,
                        event,
                        "remaining_balance",
                        self.prompt.input("remaining balance"),
                    )
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case 7:
                    pass
                case 8:
                    pass
                case 9:
                    pass
            break

        self.success_message.confirm_action(
            f"Event '{event.id}'",
            "edited",
        )

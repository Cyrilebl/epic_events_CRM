from src.views import Formatter, ErrorMessage, UserInteraction


class UtilityController:
    def __init__(self):
        self.formatter = Formatter()
        self.error_message = ErrorMessage()
        self.user_interaction = UserInteraction()

    def get_records_by_filter(self, session, model, **filters):
        """Fetch, format, and return a set of IDs based on one or multiple filters."""
        query = session.query(model)

        if filters:
            for field, value in filters.items():
                if value is None:
                    query = query.filter(getattr(model, field).is_(None))
                else:
                    query = query.filter(getattr(model, field) == value)

        records = query.all()

        model_name = model.__name__.lower()
        format = getattr(self.formatter, f"format_{model_name}s", None)
        format(records)

        return {record.id for record in records}

    def get_valid_record(self, session, model, entity_name, action, valid_ids):
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, action)

            if record_id not in valid_ids:
                self.error_message.invalid_id(entity_name)
                continue

            return session.query(model).filter_by(id=record_id).first()

from src.views import Formatter, ErrorMessage, UserInteraction


class UtilityController:
    def __init__(self):
        self.formatter = Formatter()
        self.error_message = ErrorMessage()
        self.user_interaction = UserInteraction()

    def get_records_by_filter(self, session, model, field, value=None):
        if value is None:
            records = session.query(model).filter(getattr(model, field).is_(None)).all()
        else:
            records = session.query(model).filter_by(**{field: value}).all()

        model_name = model.__name__.lower()
        getattr(self.formatter, f"format_{model_name}s", None)

        return {record.id for record in records}

    def get_valid_record(self, session, model, entity_name, action, valid_ids=None):
        while True:
            record_id = self.user_interaction.prompt_user_selection(entity_name, action)

            if valid_ids is not None and record_id not in valid_ids:
                self.error_message.invalid_id(entity_name)
                continue

            return session.query(model).filter_by(id=record_id).first()

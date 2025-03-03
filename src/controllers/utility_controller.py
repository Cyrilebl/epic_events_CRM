from src.views import Formatter


class UtilityController:
    def __init__(self):
        self.formatter = Formatter()

    def get_records_by_filter(self, session, model, field, value=None):
        if value is None:
            records = session.query(model).filter(getattr(model, field).is_(None)).all()
        else:
            records = session.query(model).filter_by(**{field: value}).all()

        model_name = model.__name__.lower()
        getattr(self.formatter, f"format_{model_name}s", None)

        return {record.id for record in records}

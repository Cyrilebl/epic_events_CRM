class DataManager:
    def add(self, session, model):
        session.add(model)
        session.commit()

    def edit_field(self, session, model, field, value):
        setattr(model, field, value)
        session.commit()

    def delete(self, session, model):
        session.delete(model)
        session.commit()

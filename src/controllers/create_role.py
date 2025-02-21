from src.models.models import Role


def create_role(session):
    manager_role = Role(name="manager")
    commercial_role = Role(name="commercial")
    support_role = Role(name="support")

    session.add(manager_role)
    session.add(commercial_role)
    session.add(support_role)
    session.commit()

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role, User, Client, Contract, Event

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

try:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    manager_role = Role(name="manager")
    commercial_role = Role(name="commercial")
    support_role = Role(name="support")

    session.add(manager_role)
    session.add(commercial_role)
    session.add(support_role)
    session.commit()

    user_manager = User(
        first_name="Bertrand",
        last_name="Lemare",
        email="bertrand.lemare@example.fr",
        role_name=manager_role.name,
    )
    user_manager.set_password("mot_de_passe")

    session.add(user_manager)
    session.commit()

    # Fetch user from the database
    saved_user = (
        session.query(User).filter_by(email="bertrand.lemare@example.fr").first()
    )

    print(saved_user.check_password("mot_de_passe"))
    print(saved_user.check_password("wrong_password"))

    events_without_assigned_support = (
        session.query(Event).filter(Event.assigned_support.is_(None)).all()
    )
    unsigned_contracts = (
        session.query(Contract).filter(Contract.signature.is_(False)).all()
    )
    unpaid_contracts = (
        session.query(Contract).filter(Contract.remaining_balance > 0).all()
    )
except Exception as e:
    print(e)

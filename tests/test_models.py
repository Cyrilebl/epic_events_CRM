import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User, Role, Client, Contract, Event


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_role_creation(session):
    role = Role(name="manager")
    session.add(role)
    session.commit()

    assert role.name == "manager"


def test_user_password_hash():
    user = User(email="test@example.com")
    user.set_password("securepassword")

    assert user.check_password("securepassword") is True
    assert user.check_password("wrongpassword") is False


def test_client_creation(session):
    client = Client(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone_number="+33 333 333 333",
        company_name="Doe Corp",
        information="test info",
        creation_date=date(2020, 1, 1),
        assigned_commercial="1",
    )
    session.add(client)
    session.commit()

    assert client.first_name == "John"


def test_contract_creation(session):
    contract = Contract(
        total_price="1000",
        remaining_balance="250",
        creation_date=date(2020, 1, 1),
        signature=True,
        client_id="1",
        assigned_commercial="1",
    )
    session.add(contract)
    session.commit()

    assert contract.total_price == 1000
    assert contract.remaining_balance == 250


def test_event_creation(session):
    event = Event(
        start_date=date(2020, 1, 1),
        end_date=date(2022, 3, 27),
        street_number="123",
        street_name="Rue de la Paix",
        postal_code="75001",
        city="Paris",
        country="France",
        attendees=50,
        notes="Important event",
        client_id="1",
        contract_id="1",
    )
    session.add(event)
    session.commit()

    assert event.city == "Paris"
    assert event.attendees == 50

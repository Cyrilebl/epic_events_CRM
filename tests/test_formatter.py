import pytest
from src.views import Formatter
from src.models import User, Client, Contract, Event


@pytest.fixture
def formatter():
    """Fixture to initialize Formatter."""

    return Formatter()


@pytest.fixture
def test_data():
    """Fixture to create all test data."""

    user1 = User(
        id=1,
        last_name="Doe",
        first_name="John",
        email="john@example.com",
        role_name="manager",
    )
    user2 = User(
        id=2,
        last_name="Smith",
        first_name="Alice",
        email="alice@example.com",
        role_name="commercial",
    )

    client1 = Client(
        id=1,
        last_name="Doe",
        first_name="Jane",
        email="jane@example.com",
        phone_number="+33 123 456 789",
        company_name="Doe Corp",
        information="VIP",
        commercial=user2,
    )
    client2 = Client(
        id=2,
        last_name="Smith",
        first_name="Alice",
        email="alice@example.com",
        phone_number="+44 987 654 321",
        company_name="Smith Company",
        information="Random info",
        commercial=user2,
    )

    contract1 = Contract(
        id=1,
        total_price=5000,
        remaining_balance=2000,
        signature=True,
        client=client1,
        commercial=user2,
    )
    contract2 = Contract(
        id=2,
        total_price=1000,
        remaining_balance=500,
        signature=False,
        client=client2,
        commercial=user2,
    )

    event1 = Event(
        id=1,
        start_date="2020-03-10",
        end_date="2020-03-12",
        street_number="10",
        street_name="Main St",
        postal_code="75001",
        city="Paris",
        country="France",
        attendees=50,
        notes="VIP event",
        client=client1,
        contract=contract1,
    )
    event2 = Event(
        id=2,
        start_date="2020-04-15",
        end_date="2020-04-16",
        street_number="20",
        street_name="Second St",
        postal_code="75002",
        city="Lyon",
        country="France",
        attendees=30,
        notes="Business meeting",
        client=client2,
        contract=contract2,
    )

    return {
        "users": [user1, user2],
        "clients": [client1, client2],
        "contracts": [contract1, contract2],
        "events": [event1, event2],
    }


def test_format_one_user(formatter, capfd, test_data):
    """Test formatting a single user."""

    formatter.format_one_user(test_data["users"][0])
    captured = capfd.readouterr()

    assert "Doe" in captured.out
    assert "John" in captured.out
    assert "xxxxxxxx" in captured.out
    assert "manager" in captured.out


def test_format_users(formatter, capfd, test_data):
    """Test formatting multiple users."""

    formatter.format_users(test_data["users"])
    captured = capfd.readouterr()

    assert "Doe" in captured.out
    assert "Smith" in captured.out
    assert "manager" in captured.out
    assert "commercial" in captured.out


def test_format_one_client(formatter, capfd, test_data):
    """Test formatting a single client."""

    formatter.format_one_client(test_data["clients"][0])
    captured = capfd.readouterr()

    assert "Doe" in captured.out
    assert "Jane" in captured.out
    assert "Doe Corp" in captured.out
    assert "+33 123 456 789" in captured.out


def test_format_clients(formatter, capfd, test_data):
    """Test formatting multiple clients."""

    formatter.format_clients(test_data["clients"])
    captured = capfd.readouterr()

    assert "Doe" in captured.out
    assert "Smith" in captured.out
    assert "VIP" in captured.out
    assert "Random info" in captured.out


def test_format_clients_empty(formatter, capfd):
    """Test formatting empty client list."""

    formatter.format_clients([])
    captured = capfd.readouterr()

    assert "No current clients." in captured.out


def test_format_one_contract(formatter, capfd, test_data):
    """Test formatting a single contract."""

    formatter.format_one_contract(test_data["contracts"][0])
    captured = capfd.readouterr()

    assert "5000" in captured.out
    assert "2000" in captured.out
    assert "True" in captured.out


def test_format_contracts(formatter, capfd, test_data):
    """Test formatting multiple contracts."""

    formatter.format_contracts(test_data["contracts"])
    captured = capfd.readouterr()

    assert "5000" in captured.out
    assert "2000" in captured.out
    assert "1000" in captured.out
    assert "500" in captured.out
    assert "True" in captured.out
    assert "False" in captured.out


def test_format_contracts_empty(formatter, capfd):
    """Test formatting empty contract list."""

    formatter.format_contracts([])
    captured = capfd.readouterr()

    assert "No contracts available." in captured.out


def test_format_one_event(formatter, capfd, test_data):
    """Test formatting a single event."""

    formatter.format_one_event(test_data["events"][0])
    captured = capfd.readouterr()

    assert "2020-03-10" in captured.out
    assert "2020-03-12" in captured.out
    assert "Main St" in captured.out
    assert "Paris" in captured.out
    assert "France" in captured.out
    assert "50" in captured.out
    assert "VIP event" in captured.out


def test_format_events(formatter, capfd, test_data):
    """Test formatting multiple events."""

    formatter.format_events(test_data["events"])
    captured = capfd.readouterr()

    assert "Paris" in captured.out
    assert "Lyon" in captured.out
    assert "50" in captured.out
    assert "30" in captured.out
    assert "VIP event" in captured.out
    assert "Business meeting" in captured.out


def test_format_events_empty(formatter, capfd):
    """Test formatting empty event list."""

    formatter.format_events([])
    captured = capfd.readouterr()

    assert "No events scheduled." in captured.out

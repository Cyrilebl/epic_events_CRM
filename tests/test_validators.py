from src.models import Validators


def test_validate_email():
    assert Validators.validate_email("test@example.com") is not None
    assert Validators.validate_email("invalid-email") is None


def test_validate_password():
    assert Validators.validate_password("StrongP4ssword") is not None
    assert Validators.validate_password("admin") is None
    assert Validators.validate_password("SHORT1") is None


def test_validate_phone_number():
    assert Validators.validate_phone_number("+33 123 456 789") is not None
    assert Validators.validate_phone_number("123-456-7890") is None


def test_validate_date():
    assert Validators.validate_date("2020-03-22 10:30 am") is not None
    assert Validators.validate_date("2020/03/22 10:30 am") is None

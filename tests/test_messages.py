import pytest
import click
from unittest.mock import patch
from src.views import ErrorMessage, SuccessMessage, UserInteraction


@pytest.fixture
def error_message():
    return ErrorMessage()


@pytest.fixture
def success_message():
    return SuccessMessage()


@pytest.fixture
def user_interaction():
    return UserInteraction()


@pytest.mark.parametrize(
    "method, args, expected_output",
    [
        ("invalid_credentials", [], "Invalid credentials."),
        ("token_expired", [], "Token expired, please log in again."),
        ("invalid_token", [], "Invalid token."),
        ("invalid_id", ["user"], "User not found. Please enter a valid ID."),
        ("invalid_format", ["email"], "Invalid email format. Please try again."),
        (
            "invalid_password",
            [],
            "Invalid password format. Must have at least one uppercase letter, one digit, and be at least 8 characters long.",
        ),
        (
            "invalid_phone_number",
            [],
            "Invalid phone number format. Use: +XX XXX XXX XXX or +XXX XXX XXX XXX.",
        ),
        ("invalid_number", [], "Invalid input. Please enter a number."),
    ],
)
def test_error_messages(error_message, method, args, expected_output):
    with patch("click.echo") as mock_echo:
        getattr(error_message, method)(*args)
        mock_echo.assert_called_once_with(
            click.style(expected_output, fg="red", bold=True)
        )


@pytest.mark.parametrize(
    "method, args, expected_output",
    [
        (
            "confirm_action",
            ["Project", "created"],
            "Project has been successfully created.",
        ),
        ("confirm_logout", [], "You have been logged out successfully."),
    ],
)
def test_success_messages(success_message, method, args, expected_output):
    with patch("click.echo") as mock_echo:
        getattr(success_message, method)(*args)
        mock_echo.assert_called_once_with(
            click.style(expected_output, fg="green", bold=True)
        )


def test_return_to_menu(user_interaction):
    with patch("click.pause") as mock_pause:
        user_interaction.return_to_menu()
        mock_pause.assert_called_once()


def test_prompt_user_selection(user_interaction):
    with patch("click.prompt", return_value=42) as mock_prompt:
        result = user_interaction.prompt_user_selection("user", "delete")
        mock_prompt.assert_called_once_with(
            click.style(
                "Enter the user ID you want to delete", fg="magenta", bold="True"
            ),
            type=int,
        )
        assert result == 42

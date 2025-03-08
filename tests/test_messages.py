import pytest
import click
from unittest.mock import patch
from src.views import ErrorMessage, SuccessMessage, UserInteraction


class TestMessages:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.error_message = ErrorMessage()
        self.success_message = SuccessMessage()
        self.user_interaction = UserInteraction()

    error_methods = [
        ("invalid_credentials", [], "Invalid credentials."),
        ("token_expired", [], "Token expired, please log in again."),
        ("invalid_token", [], "Invalid token."),
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
        ("invalid_id", ["user"], "User not found. Please enter a valid ID."),
        ("invalid_format", ["email"], "Invalid email format. Please try again."),
    ]

    @pytest.mark.parametrize("method, args,expected_output", error_methods)
    def test_error_messages_no_args(self, method, args, expected_output):
        with patch("click.echo") as mock_echo:
            getattr(self.error_message, method)(*args)
            mock_echo.assert_called_once_with(
                click.style(expected_output, fg="red", bold=True)
            )

    success_methods = [
        (
            "confirm_action",
            ["Project", "created"],
            "Project has been successfully created.",
        ),
        ("confirm_logout", [], "You have been logged out successfully."),
    ]

    @pytest.mark.parametrize("method, args,expected_output", success_methods)
    def test_success_messages(self, method, args, expected_output):
        with patch("click.echo") as mock_echo:
            getattr(self.success_message, method)(*args)
            mock_echo.assert_called_once_with(
                click.style(expected_output, fg="green", bold=True)
            )

    def test_return_to_menu(self):
        with patch("click.pause") as mock_pause:
            self.user_interaction.return_to_menu()
            mock_pause.assert_called_once()

    def test_prompt_user_selection(self):
        with patch("click.prompt", return_value=2) as mock_prompt:
            result = self.user_interaction.prompt_user_selection("user", "delete")
            mock_prompt.assert_called_once_with(
                click.style(
                    "Enter the user ID you want to delete", fg="magenta", bold="True"
                ),
                type=int,
            )
            assert result == 2

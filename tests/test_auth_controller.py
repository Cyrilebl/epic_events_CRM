from unittest.mock import MagicMock
from src.controllers.auth_controller import AuthController


class TestAuthController:
    def setup_method(self):
        self.mock_menu = MagicMock()
        self.mock_prompt = MagicMock()
        self.mock_error_message = MagicMock()
        self.mock_success_message = MagicMock()
        self.mock_token = MagicMock()
        self.mock_session = MagicMock()

        self.controller = AuthController()
        self.controller.menu = self.mock_menu
        self.controller.prompt = self.mock_prompt
        self.controller.error_message = self.mock_error_message
        self.controller.success_message = self.mock_success_message
        self.controller.token = self.mock_token

    def test_login_success(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.role.name = "admin"
        mock_user.check_password.return_value = True

        self.mock_prompt.input.side_effect = ["valid@example.com"]
        self.mock_prompt.password.return_value = "correctpassword"
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_user
        )

        self.mock_token.generate_token.return_value = "mocked_token"

        token = self.controller.login(self.mock_session)

        assert token == "mocked_token"
        self.mock_token.generate_token.assert_called_once_with(1, "admin")

    def test_login_invalid_email(self):
        self.mock_prompt.input.return_value = "invalid@example.com"
        self.mock_prompt.password.return_value = "somepassword"

        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        self.mock_prompt.try_again_yes_or_no.return_value = False

        result = self.controller.login(self.mock_session)

        assert result is None
        self.mock_error_message.invalid_credentials.assert_called_once()

    def test_logout(self):
        result = self.controller.logout()

        assert result is None
        self.mock_success_message.confirm_logout.assert_called_once()

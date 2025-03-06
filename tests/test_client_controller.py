from unittest.mock import MagicMock
from src.controllers.client_controller import ClientController


class TestClientController:
    def setup_method(self):
        self.mock_prompt = MagicMock()
        self.mock_data_manager = MagicMock()
        self.mock_success_message = MagicMock()
        self.mock_validation = MagicMock()
        self.mock_session = MagicMock()

    def _setup_controller(self):
        controller = ClientController()
        controller.prompt = self.mock_prompt
        controller.data_manager = self.mock_data_manager
        controller.success_message = self.mock_success_message
        controller.validation = self.mock_validation
        return controller

    def test_create_client(self):
        self.mock_prompt.input.side_effect = [
            "Doe",
            "John",
            "Company Inc.",
            "Some info",
        ]
        self.mock_validation.get_valid_email.return_value = "john.doe@example.com"
        self.mock_validation.get_valid_phone_number.return_value = "123456789"

        mock_user = MagicMock()
        mock_user.id = 1
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_user
        )

        controller = self._setup_controller()

        controller.create_client(self.mock_session, user_id=1)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Doe John", "created"
        )

    def test_edit_client(self):
        mock_client = MagicMock()
        mock_client.first_name = "John"
        mock_client.last_name = "Doe"
        mock_client.email = "john.doe@example.com"
        mock_client.phone_number = "123456789"
        mock_client.company_name = "Company Inc."
        mock_client.information = "Some info"

        self.mock_prompt.user_choice.return_value = 1
        self.mock_prompt.input.return_value = "NewLastName"
        self.mock_prompt.user_choice.return_value = 2
        self.mock_prompt.input.return_value = "NewFirstName"
        self.mock_prompt.user_choice.return_value = 3
        self.mock_prompt.input.return_value = "newemail@example.com"
        self.mock_prompt.user_choice.return_value = 4
        self.mock_prompt.input.return_value = "+33 333 333 333"
        self.mock_prompt.user_choice.return_value = 5
        self.mock_prompt.input.return_value = "New Company Name"
        self.mock_prompt.user_choice.return_value = 6
        self.mock_prompt.input.return_value = "New Info"

        controller = self._setup_controller()

        controller.edit_client(self.mock_session, mock_client)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Doe John", "edited"
        )

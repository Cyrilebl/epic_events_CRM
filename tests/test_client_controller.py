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

    def _test_edit_client_case(
        self, user_choice, input_value, field_name, expected_value
    ):
        mock_event = MagicMock()

        self.mock_prompt.user_choice.return_value = user_choice
        if user_choice == 3:
            self.mock_validation.get_valid_email.return_value = input_value
        if user_choice == 4:
            self.mock_validation.get_valid_phone_number.return_value = input_value
        else:
            self.mock_prompt.input.return_value = input_value

        controller = self._setup_controller()

        controller.edit_client(self.mock_session, mock_event)

        self.mock_data_manager.edit_field.assert_called_once_with(
            self.mock_session, mock_event, field_name, expected_value
        )

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

    def test_edit_client_last_name(self):
        self._test_edit_client_case(
            user_choice=1,
            input_value="Doe",
            field_name="last_name",
            expected_value="Doe",
        )

    def test_edit_client_first_name(self):
        self._test_edit_client_case(
            user_choice=2,
            input_value="John",
            field_name="first_name",
            expected_value="John",
        )

    def test_edit_client_email(self):
        self._test_edit_client_case(
            user_choice=3,
            input_value="john.doe@example.fr",
            field_name="email",
            expected_value="john.doe@example.fr",
        )

    def test_edit_client_phone_number(self):
        self._test_edit_client_case(
            user_choice=4,
            input_value="+33 123 456 789",
            field_name="phone_number",
            expected_value="+33 123 456 789",
        )

    def test_edit_client_company_name(self):
        self._test_edit_client_case(
            user_choice=5,
            input_value="Doe Corp",
            field_name="company_name",
            expected_value="Doe Corp",
        )

    def test_edit_client_information(self):
        self._test_edit_client_case(
            user_choice=6,
            input_value="VIP Client",
            field_name="information",
            expected_value="VIP Client",
        )

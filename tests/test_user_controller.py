from unittest.mock import MagicMock
from src.controllers.user_controller import UserController


class TestUserController:
    def setup_method(self):
        self.mock_prompt = MagicMock()
        self.mock_data_manager = MagicMock()
        self.mock_success_message = MagicMock()
        self.mock_validation = MagicMock()
        self.mock_session = MagicMock()

    def _setup_controller(self):
        controller = UserController()
        controller.prompt = self.mock_prompt
        controller.data_manager = self.mock_data_manager
        controller.success_message = self.mock_success_message
        controller.validation = self.mock_validation
        return controller

    def _test_edit_user_case(
        self, user_choice, input_value, field_name, expected_value
    ):
        mock_event = MagicMock()

        self.mock_prompt.user_choice.return_value = user_choice
        if user_choice in [3, 4, 5]:
            self.mock_validation.get_valid_email.return_value = (
                input_value if user_choice == 3 else None
            )
            self.mock_validation.get_valid_password.return_value = (
                input_value if user_choice == 4 else None
            )
            self.mock_prompt.role.return_value = (
                input_value if user_choice == 5 else None
            )
        else:
            self.mock_prompt.input.return_value = input_value

        controller = self._setup_controller()

        controller.edit_user(self.mock_session, mock_event)

        self.mock_data_manager.edit_field.assert_called_once_with(
            self.mock_session, mock_event, field_name, expected_value
        )

    def test_create_user(self):
        self.mock_prompt.input.side_effect = ["Doe", "John"]
        self.mock_prompt.role.return_value = "manager"
        self.mock_validation.get_valid_email.return_value = "john.doe@example.com"
        self.mock_validation.get_valid_password.return_value = "password123"

        mock_role = MagicMock()
        mock_role.name = "manager"
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            mock_role
        )

        controller = self._setup_controller()

        controller.create_user(self.mock_session)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Doe John (manager)", "created"
        )

    def test_edit_user_last_name(self):
        self._test_edit_user_case(
            user_choice=1,
            input_value="Doe",
            field_name="last_name",
            expected_value="Doe",
        )

    def test_edit_user_first_name(self):
        self._test_edit_user_case(
            user_choice=2,
            input_value="John",
            field_name="first_name",
            expected_value="John",
        )

    def test_edit_user_email(self):
        self._test_edit_user_case(
            user_choice=3,
            input_value="john.doe@example.fr",
            field_name="email",
            expected_value="john.doe@example.fr",
        )

    def test_edit_user_password(self):
        self._test_edit_user_case(
            user_choice=4,
            input_value="StrongPassword1",
            field_name="password",
            expected_value="StrongPassword1",
        )

    def test_edit_user_role(self):
        self._test_edit_user_case(
            user_choice=5,
            input_value="commercial",
            field_name="role_name",
            expected_value="commercial",
        )

    def test_delete_user(self):
        mock_user = MagicMock()
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.role_name = "manager"

        controller = self._setup_controller()

        controller.delete_user(self.mock_session, mock_user)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Doe John (manager)", "deleted"
        )

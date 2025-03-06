from unittest.mock import MagicMock
from src.controllers.event_controller import EventController


class TestEventController:
    def setup_method(self):
        self.mock_prompt = MagicMock()
        self.mock_data_manager = MagicMock()
        self.mock_success_message = MagicMock()
        self.mock_validation = MagicMock()
        self.mock_utility = MagicMock()
        self.mock_session = MagicMock()

    def _setup_controller(self):
        controller = EventController()
        controller.prompt = self.mock_prompt
        controller.data_manager = self.mock_data_manager
        controller.success_message = self.mock_success_message
        controller.validation = self.mock_validation
        controller.utility = self.mock_utility
        return controller

    def _test_edit_event_case(
        self, user_choice, input_value, field_name, expected_value
    ):
        mock_event = MagicMock()

        self.mock_prompt.user_choice.return_value = user_choice
        if user_choice in [1, 2, 8]:
            self.mock_validation.get_valid_date.return_value = (
                input_value if user_choice in [1, 2] else None
            )
            self.mock_validation.get_valid_integer.return_value = (
                input_value if user_choice == 8 else None
            )
        else:
            self.mock_prompt.input.return_value = input_value

        controller = self._setup_controller()

        controller.edit_event(self.mock_session, mock_event)

        self.mock_data_manager.edit_field.assert_called_once_with(
            self.mock_session, mock_event, field_name, expected_value
        )

    def test_create_event(self):
        self.mock_validation.get_valid_date.return_value = "2025-03-06 10:00 AM"
        self.mock_validation.get_valid_integer.return_value = 50
        self.mock_prompt.input.side_effect = [
            "123",
            "Main St",
            "10001",
            "City",
            "Country",
            "Some notes",
        ]

        mock_client = MagicMock()
        mock_client.id = 1
        self.mock_utility.get_valid_record.return_value = mock_client

        mock_contract = MagicMock()
        mock_contract.id = 1
        self.mock_utility.get_valid_record.return_value = mock_contract

        controller = self._setup_controller()

        controller.create_event(self.mock_session, user_id=1)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Event nºNone", "created"
        )

    def test_edit_event_start_date(self):
        self._test_edit_event_case(
            user_choice=1,
            input_value="2025-03-07 10:00 AM",
            field_name="start_date",
            expected_value="2025-03-07 10:00 AM",
        )

    def test_edit_event_end_date(self):
        self._test_edit_event_case(
            user_choice=2,
            input_value="2025-03-07 12:00 PM",
            field_name="end_date",
            expected_value="2025-03-07 12:00 PM",
        )

    def test_edit_event_street_number(self):
        self._test_edit_event_case(
            user_choice=3,
            input_value="456",
            field_name="street_number",
            expected_value="456",
        )

    def test_edit_event_street_name(self):
        self._test_edit_event_case(
            user_choice=4,
            input_value="Main Street",
            field_name="street_name",
            expected_value="Main Street",
        )

    def test_edit_event_postal_code(self):
        self._test_edit_event_case(
            user_choice=5,
            input_value="10001",
            field_name="postal_code",
            expected_value="10001",
        )

    def test_edit_event_city(self):
        self._test_edit_event_case(
            user_choice=6,
            input_value="New York",
            field_name="city",
            expected_value="New York",
        )

    def test_edit_event_country(self):
        self._test_edit_event_case(
            user_choice=7, input_value="USA", field_name="country", expected_value="USA"
        )

    def test_edit_event_attendees(self):
        self._test_edit_event_case(
            user_choice=8,
            input_value="100",
            field_name="attendees",
            expected_value="100",
        )

    def test_edit_event_notes(self):
        self._test_edit_event_case(
            user_choice=9,
            input_value="This is a note",
            field_name="notes",
            expected_value="This is a note",
        )

    def test_assign_support(self):
        mock_event = MagicMock()
        mock_event.id = 2
        mock_event.assigned_support = None

        mock_support = MagicMock()
        mock_support.id = 2
        self.mock_utility.get_valid_record.return_value = mock_support

        controller = self._setup_controller()

        controller.assign_support(self.mock_session)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Event nº2", "edited"
        )

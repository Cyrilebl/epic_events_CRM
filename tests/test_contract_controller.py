from unittest.mock import MagicMock
from src.controllers.contract_controller import ContractController


class TestContractController:
    def setup_method(self):
        self.mock_prompt = MagicMock()
        self.mock_data_manager = MagicMock()
        self.mock_success_message = MagicMock()
        self.mock_validation = MagicMock()
        self.mock_utility = MagicMock()
        self.mock_session = MagicMock()

    def _setup_controller(self):
        controller = ContractController()
        controller.prompt = self.mock_prompt
        controller.data_manager = self.mock_data_manager
        controller.success_message = self.mock_success_message
        controller.validation = self.mock_validation
        controller.utility = self.mock_utility
        return controller

    def _test_edit_contract_case(
        self, user_choice, input_value, field_name, expected_value
    ):
        mock_event = MagicMock()

        self.mock_prompt.user_choice.return_value = user_choice
        if user_choice in [1, 2]:
            self.mock_validation.get_valid_price.return_value = input_value
        elif user_choice == 3:
            self.mock_validation.get_valid_signature.return_value = input_value

        controller = self._setup_controller()

        controller.edit_contract(self.mock_session, mock_event)

        self.mock_data_manager.edit_field.assert_called_once_with(
            self.mock_session, mock_event, field_name, expected_value
        )

    def test_create_contract(self):
        self.mock_validation.get_valid_price.return_value = 1000
        self.mock_validation.get_valid_signature.return_value = True

        mock_client = MagicMock()
        mock_client.id = 1
        mock_client.assigned_commercial = 2
        self.mock_utility.get_valid_record.return_value = mock_client

        controller = self._setup_controller()

        controller.create_contract(self.mock_session)

    def test_edit_contract_total_price(self):
        self._test_edit_contract_case(
            user_choice=1,
            input_value="1000",
            field_name="total_price",
            expected_value="1000",
        )

    def test_edit_contract_remaining_balance(self):
        self._test_edit_contract_case(
            user_choice=2,
            input_value="256",
            field_name="remaining_balance",
            expected_value="256",
        )

    def test_edit_contract_signature(self):
        self._test_edit_contract_case(
            user_choice=3,
            input_value="yes",
            field_name="signature",
            expected_value="yes",
        )

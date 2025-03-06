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

    def test_create_contract(self):
        self.mock_validation.get_valid_price.return_value = 1000
        self.mock_validation.get_valid_signature.return_value = True

        mock_client = MagicMock()
        mock_client.id = 1
        mock_client.assigned_commercial = 2
        self.mock_utility.get_valid_record.return_value = mock_client

        controller = self._setup_controller()

        controller.create_contract(self.mock_session)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Contract nºNone", "created"
        )

    def test_edit_contract(self):
        mock_contract = MagicMock()
        mock_contract.id = 1
        mock_contract.total_price = 1000
        mock_contract.remaining_balance = 500
        mock_contract.signature = False

        self.mock_prompt.user_choice.return_value = 1
        self.mock_validation.get_valid_price.return_value = 1200
        self.mock_prompt.user_choice.return_value = 2
        self.mock_validation.get_valid_price.return_value = 300
        self.mock_prompt.user_choice.return_value = 3
        self.mock_validation.get_valid_signature.return_value = True

        controller = self._setup_controller()

        controller.edit_contract(self.mock_session, mock_contract)

        self.mock_success_message.confirm_action.assert_called_once_with(
            "Contract nº1", "edited"
        )

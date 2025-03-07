from unittest.mock import patch, MagicMock
from src.controllers.token import Token

SECRET_KEY = "test_secret_key"


class TestToken:
    def setup_method(self):
        self.token = Token()
        self.token.error_message = MagicMock()
        self.secret_key_patch = patch("src.controllers.token.SECRET_KEY", SECRET_KEY)

    def test_verify_token_valid(self):
        user_id = 1
        role_name = "manager"

        token = self.token.generate_token(user_id, role_name)
        decoded_user_id, decoded_role = self.token.verify_token(token)

        assert decoded_user_id == str(user_id)
        assert decoded_role == role_name

    def test_verify_token_invalid(self):
        invalid_token = "invalid.token"

        user_id, role = self.token.verify_token(invalid_token)

        assert user_id is None
        assert role is None
        self.token.error_message.invalid_token.assert_called_once()

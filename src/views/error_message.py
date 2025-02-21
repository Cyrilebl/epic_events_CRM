class ErrorMessage:
    def invalid_credentials(self):
        print("Invalid credentials, please try again.")

    def token_expired(self):
        print("Token expired, please log in again.")

    def invalid_token(self):
        print("Invalid token.")

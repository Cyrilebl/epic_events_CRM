import os
import jwt
import datetime
from dotenv import load_dotenv

from src.views import ErrorMessage


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class Token:
    def __init__(self):
        self.error_message = ErrorMessage()

    def generate_token(self, user_id, role_name):
        payload = {
            "sub": str(user_id),
            "role": role_name,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["sub"], payload["role"]

        except jwt.ExpiredSignatureError:
            self.error_message.token_expired()
        except jwt.InvalidTokenError:
            self.error_message.invalid_token()

        return None, None

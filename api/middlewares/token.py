import datetime
from os import getenv
from pathlib import Path  # python3 only

from dotenv import load_dotenv
from flask import request

from ...api.middlewares.base_validator import ValidationError
from ...api.utilities.messages.error_messages import jwt_errors

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
import jwt



# def generate_token(user_id):
#     """
#     Generates the Auth Token
#     :return: string
#     """
#     payload = {
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=30),
#         'iat': datetime.datetime.utcnow(),
#         'sub': user_id
#     }
#     return jwt.encode(
#         payload,
#         getenv('JWT_SECRET_KEY'),
#         algorithm='HS256'
#     )


def get_token(http_request=request):
    """Get token from request object

        Args:
            http_request (HTTPRequest): Http request object

        Returns:
            token (string): Token string

        Raises:
            ValidationError: Validation error raised when there is no token
                             or bearer keyword in authorization header
    """

    token = http_request.headers.get('Authorization')
    if not token:
        raise ValidationError({'message': jwt_errors['NO_TOKEN_MSG']}, 401)
    elif 'bearer' not in token.lower():
        raise ValidationError({'message': jwt_errors['NO_BEARER_MSG']}, 401)
        token = token.split(' ')[-1]
        return token


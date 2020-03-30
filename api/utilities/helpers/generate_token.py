import datetime

from flask_jwt_extended import create_access_token


def generate_token(user_info):
    """
    Method to generate access token
    :param user_info:
    :return: access-token
    """
    expires = datetime.timedelta(days=2)
    return create_access_token(identity=dict(
        id=user_info.id,
        email=user_info.email,
        name=user_info.name
    ), expires_delta=expires)
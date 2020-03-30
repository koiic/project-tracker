"""Module for Validation error and error handler"""
from functools import wraps

from flask import Blueprint, jsonify, request

middleware_blueprint = Blueprint('middleware', __name__)


class ValidationError(Exception):
    """Base Validation class for handling validation errors"""

    def __init__(self, error, status_code=None):
        Exception.__init__(self)
        self.status_code = 400
        self.error = error
        self.error['status'] = 'error'
        self.error['message'] = error['message']

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return self.error





#
def validate_signup_request(httprequest=request):
    # import pdb; pdb.set_trace()
    body = httprequest.get_json()
    error = {}
    keys = ['email', 'password', 'name']
    for key in keys:
        if key not in body.keys():
            error['message'] = f'{key} is required'
    if error:
        raise ValidationError(error, 400)

def validate_request(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
       validate_signup_request()
       return func(*args, **kwargs)

    return decorated_function




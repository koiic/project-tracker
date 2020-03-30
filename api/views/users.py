from flask_restplus import Resource
from flask import request

from api.middlewares.base_validator import ValidationError, validate_request
from api.models.user import bcrypt
from api.utilities.helpers.generate_token import generate_token
from api.models import User
from api.schemas.user import UserSchema
from api.utilities.helpers.response import response
from api.utilities.messages.serialization import serialization_messages
from api.utilities.messages.success import success_messages
from main import flask_api, db

schema = UserSchema()


@flask_api.route('/auth/register')
class UserSignUpResource(Resource):
	"""
	Resource class for carrying out user registration
	"""

	@validate_request
	def post(self):
		"""
		An endpoint to register a user
		"""
		request_data = request.get_json()
		print('=====>', request_data)
		user_data = schema.load_object_into_schema(request_data)

		email = request_data.get('email')
		user_exist = User.find_by_email(email)
		if user_exist:
			raise ValidationError({
				"message": serialization_messages['exists'].format('User')
			}, 409)
		user = User(**user_data)
		user.save()

		token = generate_token(user)
		data = {
			'token': token,
			'user': schema.dump(user).data
		}

		return response('success', message=success_messages['created'].format('User'), data=data, status_code=201)


@flask_api.route('/auth/login')
class UserLoginResource(Resource):
	"""
		Resource class for carrying out user authentication
	"""

	def post(self):
		"""
		An endpoint to authenticate user
		:return: dict(user data)
		"""
		request_data = request.get_json()
		email = request_data.get('email')
		password = request_data.get('password')
		user = User.find_by_email(email)
		if not user or not bcrypt.check_password_hash(user.password, password):
			raise ValidationError({'message': serialization_messages['invalid_user_data']}, 400)
		token = generate_token(user)
		data = {
			'token': token,
			'user': schema.dump(user).data
		}

		return {
			'status': 'success',
			'message': success_messages['retrieved'].format('User'),
			'data': data
			}, 200

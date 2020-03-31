# Third-party library
from flask import Flask, jsonify
from flask_restplus import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.utils import cached_property


# blueprint
from api import api_blueprint
from api.middlewares.base_validator import ValidationError, middleware_blueprint
from api.models.database import db

flask_api = Api(api_blueprint, doc='/docs')


def initialize_error_handlers(application):
	"""Initialize error handlers"""
	application.register_blueprint(middleware_blueprint)
	application.register_blueprint(api_blueprint)


# function to create app
def create_app(config):
	print('===>>> ', config.FLASK_ENV)
	app = Flask(__name__)
	CORS(app)
	app.config.from_object(config)
	app.url_map.strict_slashes = False

	# error handlers
	initialize_error_handlers(app)

	# initialise JWT
	jwt = JWTManager(app)
	jwt._set_error_handler_callbacks(flask_api)

	# bind app to db
	db.init_app(app)

	# import models
	from api import models

	# import views
	from api import views

	return app


@flask_api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
	"""Error handler called when a ValidationError Exception is raised"""

	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

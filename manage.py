# from os import getenv
import sys
import os
# Third Party Libraries
from flask import jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from livereload import Server

# Local Module Imports
from api.models.database import db
from main import create_app
from config import config

sys.path.append(os.getcwd())

config_name = os.getenv('FLASK_ENV', default='production')

# create application object
app = create_app(config[config_name])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# Entry Route
@app.route('/')
def entrypoint():
	return jsonify({
		'message': 'WELCOME THE Project Tracker APP...........',
		'status': 200
	})


server = Server(app.wsgi_app)

if __name__ == '__main__':
	server.serve(port=5000, host='0.0.0.0')

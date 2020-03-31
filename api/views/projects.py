from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from api.middlewares.base_validator import ValidationError
from api.models import Project
from api.schemas.project import ProjectSchema
from api.utilities.helpers.services import convert_date_to_date_time, assign_user
from api.utilities.helpers.response import response
from api.utilities.messages.serialization import serialization_messages
from api.utilities.messages.success import success_messages
from main import flask_api


@flask_api.route('/projects')
class ProjectResource(Resource):
	""" Resources for project creation """

	@jwt_required
	def post(self):

		""" Endpoint to create new project"""
		data = request.get_json()
		title = data.get('title')
		user = get_jwt_identity()
		project_exist = Project.find_by_title_and_user(title=title, user_id=user.get('id'))
		if project_exist:
			raise ValidationError({
				"message": serialization_messages['exists'].format('Project with title')
			}, 409)
		data['createdBy'] = user.get("id")
		project = Project()
		user_list = assign_user(data.get('assignees'))
		convert_date_to_date_time(data['due_date'])

		data['assignees'] = user_list if user_list is not None else []
		print('------------<><><><>', data['assignees'], user_list)
		assignee_ids = data['assignees']
		del data['assignees']
		schema = ProjectSchema()
		project_data = schema.load_object_into_schema(data)

		project.created_by = data['createdBy']
		project.title = data['title']
		project.description = data['description']
		project.due_date = data['due_date']
		project.assignees = assignee_ids
		print(project.assignees, '====>>>')
		project.save()

		return response('success', message=success_messages['created'].format('Project'), data=schema.dump(project).data, status_code=201)

	@jwt_required
	def get(self):
		"""
		Get all Project
		:param None:
		:return: Project object
		"""
		# user = get_jwt_identity()
		schema = ProjectSchema(many=True)
		projects = Project.get_all()
		if projects is None:
			raise ValidationError({'message': 'No Project Found'})
		projects_list = schema.dump(projects).data
		return response('success', success_messages['retrieved'].format('Projects'), projects_list)
	#
#
@flask_api.route('/projects/<int:project_id>')
class SingleProjectResource(Resource):
	""" Resource for single Project"""

	@jwt_required
	def patch(self, project_id):
		""" Endpoint to update project"""
		request_data = request.get_json()
		user = get_jwt_identity()
		project = Project.get(project_id)
		if user.get('id') != project.created_by:
			raise ValidationError({'message': 'Unauthorized user, you cannot perform this operation'})
		schema = ProjectSchema(context={'id': project_id})
		if 'assignees' in request_data:
			user_list = assign_user(request_data.get('assignees'))
			assignees = user_list if user_list is not None else []
			del request_data['assignees']
			data = schema.load_object_into_schema(request_data, partial=True)
			data['assignees'] = assignees
		else:
			print('request-data', request_data)
			data = schema.load_object_into_schema(request_data, partial=True)
		project.update_(**data)
		return response('success', message=success_messages['updated'].format('Project'), data=schema.dump(project).data, status_code=200)

	@jwt_required
	def get(self, project_id):
		"""
		Get a single project
		:param project_id:
		:return: Project object
		"""
		user = get_jwt_identity()

		schema = ProjectSchema()
		project = Project.get(project_id)
		if project is None:
			raise ValidationError({'message': 'Project not found'})
		project = schema.dump(project).data
		return response('success', success_messages['retrieved'].format('Project'), project)

	@jwt_required
	def delete(self, project_id):
		"""
		Delete a single project
		:param project_id:
		:return:
		"""
		user = get_jwt_identity()
		project_exists = Project.find_by_id_and_user(project_id, user.get('id'))
		if project_exists is None:
			raise ValidationError({'message': 'Project thing not found'})
		Project.delete_item(project_exists)

		return {
			'status':  'success',
			'message': 'Project deleted successfully'
		}


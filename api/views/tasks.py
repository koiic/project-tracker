from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from api.middlewares.base_validator import ValidationError
from api.models import Project, Task
from api.schemas.task import TaskSchema
from api.utilities.helpers.services import convert_date_to_date_time, check_assignee, check_date_difference, \
	assign_user
from api.utilities.helpers.response import response
from api.utilities.messages.serialization import serialization_messages
from api.utilities.messages.success import success_messages
from main import flask_api


@flask_api.route('/tasks')
class TaskResource(Resource):
	""" Resources for task creation """

	@jwt_required
	def post(self):
		""" Endpoint to create new Task"""

		data = request.get_json()
		title = data.get('title')
		formatted_date = convert_date_to_date_time(data['due_date'])
		print(type(formatted_date))
		schema = TaskSchema()
		project_id = data['projectId']
		project = Project.get_or_404(project_id)
		task_exist = Task.find_by_title_and_project_id(title=title, project_id=project.id)
		if task_exist:
			raise ValidationError({
				"message": serialization_messages['exists'].format('Task with title')
			}, 409)
		if not check_date_difference(formatted_date, project.due_date):
			raise ValidationError({
				"message": "Tasks cannot be created under this project because of dat difference"
			}, 401)
		assignee_list = check_assignee(data.get('task_assignees'), project.assignees)
		if assignee_list is not None:
			user_list = assign_user(assignee_list)
			data['task_assignees'] = user_list
		else:
			data['task_assignees'] = []
		print(data['task_assignees'], '+++++++++++')
		print(data['task_assignees'], '8888888>>>>>')
		assignee_ids = data['task_assignees'] if data['task_assignees'] is not None else []
		del data['task_assignees']
		task_data = schema.load_object_into_schema(data)

		task = Task()
		task.title = data['title']
		task.description = data['description']
		task.due_date = data['due_date']
		task.task_assignees = assignee_ids
		task.project_id = project.id
		print(project.assignees, '====>>>')
		task.save()

		task.save()

		return response('success', message=success_messages['created'].format('Task'),
								data=schema.dump(task).data, status_code=201)

	@jwt_required
	def get(self):
		"""
		Get all tasks
		:param None:
		:return: Tasks List
		"""
		# user = get_jwt_identity()
		schema = TaskSchema(many=True)
		tasks = Task.get_all()
		if tasks is None:
			raise ValidationError({'message': 'No Task Found'})
		return response('success', success_messages['retrieved'].format('Tasks'), schema.dump(tasks).data)


#
#
@flask_api.route('/tasks/<int:task_id>')
class SingleTaskResource(Resource):
	""" Resource for single Task"""

	@jwt_required
	def patch(self, task_id):
		""" Endpoint to update task"""
		request_data = request.get_json()
		user = get_jwt_identity()
		task = Task.get_or_404(task_id)
		schema = TaskSchema(context={'id': task_id})

		if 'task_assignees' in request_data:
			project = Project.get_or_404(task.project_id)
			assignee_list = check_assignee(request_data.get('task_assignees'), project.assignees)
			if assignee_list is not None:
				user_list = assign_user(assignee_list)
				assignees = user_list if user_list is not None else []
				del request_data['task_assignees']
				data = schema.load_object_into_schema(request_data, partial=True)
				data['task_assignees'] = assignees
				print('i got here', data)
				task.update_(**data)
		else:
			data = schema.load_object_into_schema(request_data, partial=True)
			task.update_(**data)
		return response('success', message=success_messages['updated'].format('Task'),
						data=schema.dump(task).data, status_code=200)

	@jwt_required
	def get(self, task_id):
		"""
		Get a single task
		:param task_id:
		:return: Task object
		"""
		user = get_jwt_identity()

		schema = TaskSchema()
		task = Task.get(task_id)
		if task is None:
			raise ValidationError({'message': 'Task not found'})
		return response('success', success_messages['retrieved'].format('Task'), schema.dump(task).data)

	@jwt_required
	def delete(self, task_id):
		"""
		Delete a single task
		:param task_id:
		:return:
		"""
		user = get_jwt_identity()
		task_exists = Task.find_by_id(task_id)
		if task_exists is None:
			raise ValidationError({'message': 'Task not found'})
		Project.delete_item(task_exists)

		return {
			'status': 'success',
			'message': 'Task deleted successfully'
		}


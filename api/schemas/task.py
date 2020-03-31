from api.utilities.validators.string_length_validator import min_length_validator, empty_string_validator
from api.utilities.validators.name_validator import validate_name

from .user import UserSchema
from .base import BaseSchema
from marshmallow import fields, validates
from marshmallow.validate import Length, Range

from ..models import Task


class TaskSchema(BaseSchema):
	title = fields.String(required=True, validate=Length(max=60))
	description = fields.String(dump_to="description", load_from="description")

	project_id = fields.Int(
		load_from="projectId",
		dump_to="projectId")

	task_assignees = fields.List(fields.Nested(
		UserSchema, dump_to="task_assignees", dump_only=True
	))

	due_date = fields.DateTime(dump_to="dueDate", load_from="due_date")

	class Meta:
		model = Task

	@validates('description')
	def name_validator(self, value):
		min_length_validator(value)

	@validates('title')
	def name_validator(self, value):
		validate_name(value)
		empty_string_validator(value)

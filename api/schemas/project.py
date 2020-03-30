from api.utilities.validators.string_length_validator import min_length_validator, empty_string_validator
from api.utilities.validators.name_validator import validate_name

from .user import UserSchema
from .task import TaskSchema
from .base import BaseSchema
from marshmallow import fields, validates
from marshmallow.validate import Length, Range

from ..models import Project


class ProjectSchema(BaseSchema):
    title = fields.Str(required=True, validate=Length(max=60))
    description = fields.Str(dump_to="description", load_from="description")

    tasks = fields.List(fields.Nested(
        TaskSchema,
        only=['title', 'description', "due_date"],
        dump_to='tasks'))

    assignees = fields.List(fields.Nested(
        UserSchema, only=['email', 'id', 'name'], load_from="assignees"))

    due_date = fields.DateTime(dump_to="dueDate", load_from="due_date")
    # created_by = fields.Int(
    #     dump_to='createdBy',
    #     load_from='createdBy')

    user = fields.Nested(
        UserSchema,
        only=['email', 'name'],
        dump_to='manager'
    )

    class Meta:
        model = Project

    @validates('description')
    def name_validator(self, value):
        min_length_validator(value)

    @validates('title')
    def name_validator(self, value):
        validate_name(value)
        empty_string_validator(value)

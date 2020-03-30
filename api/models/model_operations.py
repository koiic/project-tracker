from datetime import datetime
import re
from flask import request

from api.middlewares.base_validator import ValidationError
from api.models.database import db


class ModelOperations(object):
	"""Mixin class with generic model operations."""

	def save(self):
		"""
			Save a Model Instance
			:return:
		"""
		db.session.add(self)
		db.session.commit()
		return self

	def update_(self, **kwargs):
		"""
			update entries
		"""
		for field, value in kwargs.items():
			setattr(self, field, value)
			self.updated_at = datetime.utcnow()
		db.session.commit()

	@classmethod
	def get(cls, id):
		"""
			return entries by id
		"""
		value = cls.query.filter_by(id=id, deleted=False).first()
		if value is None:
			raise ValidationError({'message': f'{cls.__name__} not found'})
		return value

	@classmethod
	def get_all(cls):
		"""
			return all entries
		"""
		value = cls.query.filter_by(deleted=False).order_by(cls.due_date.asc()).all()
		if value is None:
			raise ValidationError({'message': f'{cls.__name__} not found'})
		return value

	@classmethod
	def find_by_email(cls, email):
		"""
			Find user by email
		"""
		if email:
			return cls.query.filter_by(email=email).first()
		return {
				'message': 'email field is required',
				'status': 'Failed'
				}, 400

	@classmethod
	def find_by_id(cls, id):
		"""
			Find entries by id
		"""
		if id:
			return cls.query.filter_by(id=id).first()
		return {
			'message': 'id field is required',
			'status': 'Failed'
			}, 400

	def delete_item(self):
		"""
		Deletes a database instance
		:return: None
		"""

		db.session.delete(self)
		db.session.commit()

	@classmethod
	def get_or_404(cls, instance_id):
		"""
			Gets an instance by id or returns 404
			:param instance_id: the id of instance to get
			:return: return instance or 404
		"""
		instance = cls.query.filter_by(id=instance_id).first()
		if not instance:
			raise ValidationError(
				{
					'message':
						f'{re.sub(r"(?<=[a-z])[A-Z]+", lambda x: f" {x.group(0).lower()}", cls.__name__)} not found'
					# noqa
				},
				404)
		return instance

	@classmethod
	def bulk_create(cls, raw_list):
		"""
		Save raw list of records to database
		Parameters:
			raw_list(list): List of records to be saved to database
		"""
		resource_list = [cls(**item) for item in raw_list]
		db.session.add_all(resource_list)
		db.session.commit()

		return resource_list

	@classmethod
	def find_or_create(cls, data, **kwargs):
		"""
			Finds a model instance or creates it
		"""
		instance = cls.query.filter_by(**kwargs).first()
		if not instance:
			instance = cls(**data).save()
		return instance

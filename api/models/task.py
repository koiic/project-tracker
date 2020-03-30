from .base import BaseModel
from .database import db

task_owners = db.Table('task_owners',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
                          )


class Task(BaseModel):
	"""
    Model For Task
    """
	__tablename__ = 'tasks'

	title = db.Column(db.String(60), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	meta_data = db.Column(db.JSON, nullable=True)
	due_date = db.Column(db.DateTime, nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
	task_assignees = db.relationship('User', secondary=task_owners, lazy='subquery',
	                         backref=db.backref('tasks', lazy=True))

	def get_child_relationship(self):
		"""
		Method to get all child relationships a model has. Override in the
		subclass if the model has child models.
		"""
		return None

	def __repr__(self):
		return '<Task {}>'.format(self.title)

	@staticmethod
	def find_by_title_and_project_id(title, project_id):
		return Task.query.filter_by(title=title, project_id=project_id).first()

	@staticmethod
	def find_by_id(task_id):
		return Task.query.filter_by(id=task_id, deleted=False).first()

	@staticmethod
	def get_all_tasks():
		return Task.query.filter(Task.deleted == False).order_by(
			Task.due_date.asc()).all()

	# soft delete a task
	@staticmethod
	def delete_task(id):
		task = Task.query.get(id)
		if Task:
			Task.deleted = True
		db.session.commit()


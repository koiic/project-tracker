from .base import BaseModel
from .database import db

project_owners = db.Table('project_owners',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True)
                          )


class Project(BaseModel):
	"""
    Model For Project
    """
	__tablename__ = 'projects'

	title = db.Column(db.String(60), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	due_date = db.Column(db.Date, nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
	assignees = db.relationship('User', secondary=project_owners,
						backref=db.backref('projects', lazy=True))
	tasks = db.relationship('Task', backref=db.backref('projects', lazy=True))
	user = db.relationship('User')

	def get_child_relationship(self):
		"""
		Method to get all child relationships a model has. Override in the
		subclass if the model has child models.
		"""
		return None

	def __repr__(self):
		return '<Project {}>'.format(self.title)

	@staticmethod
	def find_by_title_and_user(title, user_id):
		return Project.query.filter_by(title=title, created_by=user_id).first()

	@staticmethod
	def find_by_id_and_user(project_id, user_id):
		return Project.query.filter_by(id=project_id, created_by=user_id, deleted=False).first()

	@staticmethod
	def get_all_Project(user_id):
		return Project.query.filter(Project.created_by == user_id, Project.deleted == False).order_by(
			Project.due_date.asc()).all()


	# @staticmethod
	# def get_tasks(rank):
	# 	return Project.query.filter(Project.rank >= rank).all()

	# soft delete a Project
	@staticmethod
	def delete_Project_thing(id):
		project = Project.query.get(id)
		if Project:
			Project.deleted = True
		db.session.commit()

	@staticmethod
	def get_by_category(category_id, user_id):
		return Project.query.filter_by(category_id=category_id, user_id=user_id, deleted=False).all()

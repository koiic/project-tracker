from .base import BaseModel
from .database import db
from flask_bcrypt import Bcrypt
from sqlalchemy.event import listens_for


bcrypt = Bcrypt()


class User(BaseModel):
    """
    Model for User
    """
    __tablename__ = 'users'

    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def get_child_relationship(self):
        """
        Method to get all child relationships a model has. Override in the
        subclass if the model has child models.
        """
        return None

    def __repr__(self):
        return '<User {}>'.format(self.email)

@listens_for(User, 'before_insert')
def hash_password(mapper, connect, target):
    """
    :param mapper:
    :param connect:
    :param target:
    :return: None
    """
    target.password = bcrypt.generate_password_hash(target.password, 8).decode('utf-8')


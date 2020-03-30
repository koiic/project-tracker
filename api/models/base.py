#sqlAlchemy Instance
from datetime import datetime

from api.models.model_operations import ModelOperations
from .database import db

class BaseModel(db.Model, ModelOperations):
    """
    Base Model for all database models
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

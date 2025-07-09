from app.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Issue(BaseModel, Base):
    __tablename__ = 'issues'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    title = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    status = Column(String(20), default='open', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='issues', lazy='select')
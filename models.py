from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    checks = relationship('Check', backref='url')

class URLStatus(Base):
    __tablename__ = 'url_status'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Integer, nullable=False)
    is_up = Column(Boolean, default=True)
    checked_at = Column(DateTime, default=datetime.now)

    url = relationship('URL', back_populates='status')

URL.status = relationship('URLStatus', order_by=URLStatus.checked_at.desc(), back_populates='url')
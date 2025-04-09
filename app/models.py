from datetime import datetime
from sqlalchemy import Column, Integer, String, DATETIME
from app.database import Base

class User(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    post_heading = Column(String(50), nullable=False)
    post_description = Column(String(50), nullable=False)
    created_at = Column(DATETIME, default= datetime.now())
    modified_at = Column(DATETIME, default=datetime.now(), onupdate=datetime.now())



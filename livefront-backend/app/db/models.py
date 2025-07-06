from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Text, DateTime
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class School(Base):
    __tablename__ = "Schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

    users = relationship("User", back_populates="school")

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("Schools.id"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(String, nullable=False)

    school = relationship("School", back_populates="users")

class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(String, nullable=False)

class ConversationHistory(Base):
    __tablename__ = "Conversation_History"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    conversation_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)   # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class ReferralFAQ(Base):
    __tablename__ = "Referral_FAQs"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
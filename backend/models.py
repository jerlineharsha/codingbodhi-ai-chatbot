from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey

from database import Base


# =========================
# USERS
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)

    # user or admin
    role = Column(String(20), default="user", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# CONVERSATIONS
# =========================

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# =========================
# MESSAGES
# =========================

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False
    )

    # user or bot
    sender = Column(String(20), nullable=False)

    message = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# FEEDBACK
# =========================

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    message_id = Column(
        Integer,
        ForeignKey("messages.id"),
        nullable=False
    )

    # Example: 1 = negative, 5 = excellent
    rating = Column(Integer, nullable=True)

    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# UNANSWERED QUESTIONS
# =========================

class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    question = Column(Text, nullable=False)

    resolved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
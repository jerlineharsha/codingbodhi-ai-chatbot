import logging
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from llm import ChatGenerationError, generate_response
from models import Conversation, Message, User
from schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    ConversationMessage,
)


logger = logging.getLogger(__name__)

app = FastAPI(
    title="CodingBodhi AI Chatbot API",
    description="Backend API for the CodingBodhi AI Chatbot",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


def initialize_database() -> None:
    if engine.dialect.name == "postgresql":
        with engine.begin() as connection:
            connection.execute(
                text(
                    "SELECT pg_advisory_xact_lock("
                    "hashtext('codingbodhi_schema_init'))"
                )
            )
            Base.metadata.create_all(bind=connection)
        return

    Base.metadata.create_all(bind=engine)


initialize_database()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    conversation = None
    history = []

    if request.conversation_id is not None:
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == request.user_id,
            )
            .first()
        )
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")

        history = [
            {"sender": message.sender, "message": message.message}
            for message in (
                db.query(Message)
                .filter(Message.conversation_id == conversation.id)
                .order_by(Message.id.desc())
                .limit(20)
                .all()[::-1]
            )
        ]

    try:
        bot_response = generate_response(request.message, history)
    except ChatGenerationError as error:
        logger.exception("Chat response generation failed")
        raise HTTPException(status_code=503, detail=str(error)) from error

    try:
        if user is None:
            user = User(id=request.user_id, role="user")
            db.add(user)
            db.flush()

        if conversation is None:
            conversation = Conversation(
                user_id=user.id,
                title=request.message[:50],
            )
            db.add(conversation)
            db.flush()

        db.add_all(
            [
                Message(
                    conversation_id=conversation.id,
                    sender="user",
                    message=request.message,
                ),
                Message(
                    conversation_id=conversation.id,
                    sender="bot",
                    message=bot_response,
                ),
            ]
        )
        db.commit()
        db.refresh(conversation)
    except Exception:
        db.rollback()
        logger.exception("Could not save chat messages")
        raise

    return ChatResponse(
        conversation_id=conversation.id,
        user_message=request.message,
        bot_message=bot_response,
    )


@app.get(
    "/conversations/{conversation_id}/messages",
    response_model=ConversationHistoryResponse,
)
def get_conversation_messages(
    conversation_id: int,
    user_id: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.id.asc())
        .all()
    )
    return ConversationHistoryResponse(
        conversation_id=conversation.id,
        messages=[
            ConversationMessage(
                sender=message.sender,
                message=message.message,
                created_at=message.created_at.isoformat(),
            )
            for message in messages
        ],
    )


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

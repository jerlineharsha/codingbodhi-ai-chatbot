from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    user_id: int = Field(gt=0)
    conversation_id: int | None = Field(default=None, gt=0)
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    bot_message: str


class ConversationMessage(BaseModel):
    sender: str
    message: str
    created_at: str


class ConversationHistoryResponse(BaseModel):
    conversation_id: int
    messages: list[ConversationMessage]

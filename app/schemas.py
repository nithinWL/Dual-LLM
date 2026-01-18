from pydantic import BaseModel
from typing import List


class Request(BaseModel):
    """Request body for /run-session"""
    subject: str
    num_pairs: int = 5


class QApair(BaseModel):
    """Single question–answer pair"""
    id: int
    question: str
    answer: str


class Response(BaseModel):
    """Response returned by /run-session"""
    subject: str
    num_pairs: int
    pairs: List[QApair]


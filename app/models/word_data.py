from pydantic import BaseModel


class WordData(BaseModel):
    word: str


class WordInfo(BaseModel):
    imageUrl: str
    explanation: str
    story: str
    fact: str

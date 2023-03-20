from typing import List, Field
from pydantic import BaseModel


class WordData(BaseModel):
    """
    A Pydantic model for the word data input.

    Attributes:
    - word (str): The word to be looked up.
    """
    word: str


class WordInfo(BaseModel):
    """
    A Pydantic model for the word information output.

    Attributes:
    - imageUrl (str): The URL of the image associated with the word.
    - explanation (str): An explanation of the word in a simple way that a 4-year-old child can understand.
    - story (str): A short and simple story for a 4-year-old child that includes the word.
    - fact (str): An interesting and simple fact about the word that a 4-year-old child would enjoy.
    """
    imageUrl: str
    explanation: str
    story: str
    fact: str


class WordListResponse(BaseModel):
    words: List[WordData]


class WordDetailsListResponse(BaseModel):
    words: List[WordInfo]


class GalleryWordsQueryParams(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

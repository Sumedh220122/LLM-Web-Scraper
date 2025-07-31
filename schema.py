"""
Model for quotes schema
"""

from typing import List
from pydantic import BaseModel

class Quote(BaseModel):
    author_name: str
    quote: str
    tags: List[str]

class Quotes(BaseModel):
    quotes: List[Quote]        
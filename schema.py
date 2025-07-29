from pydantic import BaseModel, Field

class SchemaReviews(BaseModel):
    author_name: str
    rating: float
    review_content: str

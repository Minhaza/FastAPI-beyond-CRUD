from typing import Optional
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class ReviewModel(BaseModel):
    id: uuid.UUID
    review_text: str
    rating: int = Field(le=5)
    user_id: Optional[uuid.UUID] 
    book_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime 
    
class ReviewCreateModel(BaseModel):
    review_text: str
    rating: int = Field(le=5)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "review_text": "Nice one",
                "rating": 5
            }
        }
    }
    
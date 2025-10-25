# Consultar y crear datos
import datetime
from pydantic import BaseModel, Field, field_validator


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str
    
class MovieCreate(BaseModel):
    id: int
    title: str
    overview: str = Field(min_length=15, max_length=500)
    year: int = Field(le=datetime.date.today().year, ge=1900)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "My Movie",
                "overview": "This is a brief description of my movie.",
                "year": 2010,
                "rating": 8.8,
                "category": "Sci-Fi"
            }
        }
    }

    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 5 or len(value) > 15:
            raise ValueError('Title must be between 5 and 15 characters long')
        return value
    
    
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str   


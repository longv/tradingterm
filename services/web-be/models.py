import uuid
from datetime import datetime
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, root_validator


class TradeEvent(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": {
                    "$oid": "674c1d48a13debafe2e364c9"
                },
                "symbol": "2CRSI.FR",
                "sectype": "E",
                "last": 5.119999885559082,
                "ema": 1.9310302225654525,
                "timestamp": {
                    "$date": "2021-11-08T09:44:05.771Z"
                }
            }
        }
    )

    id: str = Field(alias="_id")
    symbol: str = Field(validation_alias="id", serialization_alias="symbol")
    sectype: str = Field(...)
    last: float = Field(...)
    ema: float = Field(...)
    timestamp: datetime = Field(...)

    @root_validator(pre=True)
    def convert_objectid(cls, values):
        # Convert `_id` from ObjectId to string
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["_id"] = str(values["_id"])
        return values


class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }

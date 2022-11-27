from pydantic import BaseModel
from typing import Optional

class Tweet(BaseModel):
    keyword: str
    no_tweet: int

class TweetResponse(BaseModel):
    tweet: str
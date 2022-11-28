from pydantic import BaseModel


class Tweet(BaseModel):
    keyword: str
    no_tweet: int


class ErrorResponse(BaseModel):
    status_code: int
    message: str


class WordCloudResponse(BaseModel):
    query: str
    total: int
    image: str




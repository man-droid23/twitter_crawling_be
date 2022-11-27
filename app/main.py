from fastapi import FastAPI, HTTPException, status
from . import logic
from fastapi.responses import JSONResponse
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/search')
async def keyword_search(keyword: str, no_tweet: int):
    try:
        result = logic.keyword_search(keyword, no_tweet)
        if result:
            # result = json.dumps(result)
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




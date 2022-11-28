from fastapi import FastAPI, HTTPException, status, Request

from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.crawling import keyword_search, get_trends_twitter
from app.schemas import WordCloudResponse, ErrorResponse

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

app.mount("/tmp", StaticFiles(directory="/tmp"), name="tmp")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get('/generate-word-cloud',
         response_model=WordCloudResponse)
async def generate_word_cloud(keyword: str, total_tweet: int, request: Request):
    try:
        if total_tweet <= 100 or total_tweet < 10:
            result = keyword_search(keyword, total_tweet)
            if result:
                return WordCloudResponse(
                    query=keyword,
                    total=total_tweet,
                    image=str(request.base_url) + result
                )
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Data Tidak Ditemukan")
        else:
            if total_tweet <= 100:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Total tweet tidak boleh lebih dari 100")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total tweet kurang dari 10")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get('/trends')
async def get_trends():
    try:
        result = get_trends_twitter()
        if result:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

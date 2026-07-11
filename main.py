from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from amazon import crawl_amazon
from agent import crawl_article

app = FastAPI()

class CrawlRequest(BaseModel):
    url: str


def process_url(url: str) -> dict:
    domain = urlparse(url).netloc.lower()
    if "amazon.com" in domain:
        return crawl_amazon(url)
    return crawl_article(url)


@app.get("/")
def home():
    return {
        "message": "BrightEdge crawler API is running"
    }


@app.post("/crawl")
def crawl(request: CrawlRequest):
    try:
        result = process_url(request.url)
        return {
            "success": True,
            "result": result,
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
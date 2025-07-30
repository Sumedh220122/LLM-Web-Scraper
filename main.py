import asyncio
import pprint
from llm_extractor import LLMExtractor
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/reviews/")
async def get_reviews(
    url: str = Query(..., description="URL of the page to scrape")
):
    try:
        extractor = LLMExtractor()
        quotes = await extractor.extract_quotes(url)
        
        total_quotes = [sum(len(quote.quotes)) for quote in quotes]

        return {"success": True, "data": {"reviews_count" : total_quotes, "reviews" : quotes}}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)

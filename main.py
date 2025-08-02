from llm_extractor import LLMExtractor
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/api/v1/quotes/")
async def get_reviews(
    url: str = Query(..., description="URL of the page to scrape")
):
    try:
        extractor = LLMExtractor()
        quotes = await extractor.extract_quotes(url)
        
        return {"success": True, "data": {"reviews_count" : len(quotes), "reviews" : quotes}}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)


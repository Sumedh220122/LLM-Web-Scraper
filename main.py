import asyncio
import pprint

from llm_extractor import extract
from schema import SchemaReviews
from scraping import ascrape_playwright
from fastapi import FastAPI, Query
import uvicorn

import re

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

token_limit = 8000

async def scrape_with_playwright(url: str, tags, **kwargs):
    html_content = await ascrape_playwright(url, tags)

    print("Extracting content with LLM")

    extracted_list = []

    for i in range(0, len(html_content), token_limit):
        html_content_fits_context_window_llm = html_content[i: i + token_limit]

        extracted_content = extract(**kwargs,
                                    content=html_content_fits_context_window_llm)

        if extracted_content != {}:
            extracted_list.append(extracted_content.dict())

    return extracted_list


@app.get("/api/reviews/")
async def get_reviews(
    url: str = Query(..., description="URL of the page to scrape")
):
    print(url)
    try:
        tags = ["div", "p", "span", "a"]  # HTML tags to scrape
        results = await scrape_with_playwright(
            url=url, tags=tags, schema_pydantic=SchemaReviews
        )
        return {"success": True, "data": {"reviews_count" : len(results), "reviews" : results}}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)

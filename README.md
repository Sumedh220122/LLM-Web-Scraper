# LLM Web Scraper

This project provides a tool for automating the process of web scraping and structured information extraction from websites using Large Language Models (LLMs). It is designed to extract quotes (or similar structured data) from paginated web pages, leveraging Playwright for browser automation and Cohere LLM (via LangChain) for intelligent content parsing.

## Project Structure

- **llm_extractor.py**: Main logic for extracting structured data (quotes) from websites using the Cohere LLM. Handles pagination, prompt construction, and schema-based extraction.
- **scraping.py**: Utilities for scraping web pages using Playwright and BeautifulSoup, including HTML cleaning, tag extraction, and content chunking.
- **schema.py**: Defines the Pydantic models (schema) for the extracted data (quotes, authors, tags).
- **prompts.py**: Contains prompt templates for instructing the LLM on extraction, tag identification, and CSS selector generation.
- **main.py**: FastAPI server exposing endpoints for triggering the extraction process.
- **requirements.txt**: Python dependencies for the project.

## Features

- **Automated Web Scraping**: Uses Playwright to interact with and scrape dynamic web pages.
- **LLM-Powered Extraction**: Employs Cohere LLM (via LangChain) to extract structured data from unstructured HTML.
- **Pagination Handling**: Automatically detects and follows pagination links to extract data from multiple pages.
- **API Interface**: Exposes a FastAPI endpoint for programmatic access.

## Installation

1. Clone the repository and navigate to the project directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```
4. Set up your environment variables (e.g., Cohere API key) in a `.env` file if required by your LLM provider.

## Usage

### Running the API Server

Start the FastAPI server with Uvicorn:
```bash
uvicorn main:app --host 127.0.0.1 --port 5049 --log-level debug
```

### API Endpoints

- **POST `/api/v1/quotes/`**
  - **Query Parameter:** `url` (string) — The URL of the page to scrape.
  - **Description:** Extracts quotes from the given URL (and paginated pages).
  - **Response:**
    - `success`: Boolean
    - `data`: Object containing `reviews_count` and a list of extracted `reviews` (quotes)
    - `error`: Error message if extraction fails

## Notes
- The extraction logic is tailored for quote-style websites but can be adapted for other schemas by modifying `schema.py` and the prompt templates in `prompts.py`.
- Ensure your Cohere API key (or other LLM provider credentials) is set up in your environment.
- Playwright requires Chromium to be installed (handled by `playwright install`).


 




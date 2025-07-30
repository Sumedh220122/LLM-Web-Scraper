"""
Module containing website scraping utilities
"""

import requests
from typing import List
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def scrape_website(url: str) -> str:
    """Scrape the website at the given URL and return its HTML content."""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            page_source = await page.content()
        except (ConnectionError, ValueError) as e:
            return f"Connection error: {e}"
        finally:
            await browser.close()
    
    return page_source

def extract_body_content(html_content) -> str:
    """Extract the body content from the HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content) -> str:
    """Clean the body content by removing unwanted tags."""
    soup = BeautifulSoup(body_content, 'html.parser')
    
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator = "\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def extract_tags(url: str) -> List[str]:
    """Extract all a tags from the given html content to identify potential paginated related ones"""    
    tags = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    a_tags = soup.find_all("a")

    for tag in a_tags:
        tags.append(str(tag))

    return tags

async def click_and_scrape(url: str, selector: str) -> str:
    """Click selectors, navigate to the next page and extract it's url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        await page.wait_for_load_state("networkidle")

        try:
            await page.click(selector) 
            await page.wait_for_load_state("networkidle")

            updated_url = page.url

            return updated_url

        except Exception as e:
            print("Error clicking pagination link:", e)

        await browser.close()

def chunk_content(content: str, chunk_size: int = 6000) -> List[str]:
    """Chunk the content into smaller parts."""
    return [
        content[i: i + chunk_size] for i in range(0, len(content), chunk_size)
    ]
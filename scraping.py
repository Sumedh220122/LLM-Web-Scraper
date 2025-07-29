import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"]):
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content, tags: list[str]):
   
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []


    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            if tag == "a":
                href = element.get('href')
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
                else:
                    text_parts.append(element.get_text())
            else:
                text_parts.append(element.get_text())

    return ' '.join(text_parts)


def remove_unessesary_lines(content):
    lines = content.split("\n")

    stripped_lines = [line.strip() for line in lines]

    non_empty_lines = [line for line in stripped_lines if line]

    seen = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in seen or seen.add(line))]

    cleaned_content = "".join(deduped_lines)

    return cleaned_content


async def ascrape_playwright(url, tags: list[str] = ["div", "p", "span"]) -> str:
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()

            results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(
                page_source), tags))

            print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results
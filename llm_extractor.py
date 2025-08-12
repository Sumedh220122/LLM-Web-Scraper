"""
The module for main LLM extractor that extracts quotes from a quote website
"""

from typing import List
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

from scraping import (
    scrape_website, extract_body_content, 
    clean_body_content, chunk_content, 
    click_and_scrape, extract_tags
)
from prompts import (
    get_quote_extraction_prompt, get_tag_extraction_prompt,
    get_selector_extraction_prompt
)

from schema import Quotes, Quote

load_dotenv()

class LLMExtractor:
    def __init__(self):
        self.llm = ChatCohere(
            temperature=0
        )
    
    def parse_quotes_with_llm(self, content: List[str]) -> List[Quotes]:
        """
        Parse quotes from website url content
        Params:
            content: List[str] -> The website content in chunks to be parsed
        returns:
            parsed_results: Quotes -> The parsed quote objects 
        """
        
        template = get_quote_extraction_prompt()

        parser = PydanticOutputParser(pydantic_object=Quotes)

        prompt = PromptTemplate(
            input_variables=["body_content"],
            partial_variables={"schema": parser.get_format_instructions()},
            template=template,
        )

        chain = prompt | self.llm | parser

        parsed_results = []

        for _, chunk in enumerate(content):
            response = chain.invoke({
                "body_content": chunk,
            })

            parsed_results.append(response)

        return parsed_results
    
    def find_pagination_tag(self, tags) -> str:
        """
        Identify the tag/element that is responsible for pagination
        Params:
            tags: List[str] -> List of "a" tags extracted from the given url
        Returns:
            tag: The tag/element that is responsible for pagination
        """
        template = get_tag_extraction_prompt()

        prompt = ChatPromptTemplate.from_template(template)
        
        chain = prompt | self.llm

        response = chain.invoke({
            "tags": tags,
        })

        return response.content

    def find_query_selector(self, tag: str) -> str:
        """
        Identify the css selector for the tag responsible for pagination
        Params:
            tag: str -> The tag/element that is responsible for pagination
        Returns:
            selector: str -> the css selector for the tag.
        """
        template = get_selector_extraction_prompt()

        prompt = ChatPromptTemplate.from_template(template)
        
        chain = prompt | self.llm

        response = chain.invoke({
            "tag": tag,
        })

        return response.content
    
    async def get_url_with_pagination(self, url: str) -> str:
        """
        Get the new url after performing pagination
        Params:
            url: str -> The url of the website
        Returns:
            new_url: str -> The url after pagination
        """
        tags = await extract_tags(url)

        tags_str = "\n".join(tags)
        pagination_tag = self.find_pagination_tag(tags_str)
        query_selector = self.find_query_selector(pagination_tag)

        print(f"Pagination tag found: {pagination_tag}")
        print(f"Query selector for tag: {query_selector}")

        new_url = await click_and_scrape(url, query_selector)

        print("New url after pagination: ", new_url)

        return new_url
    
    async def extract_quotes(self, url: str, max_pages: int = 2) -> List[Quote]:
        """
        Main function to recursively extract paginated quotes from a given website
        Params:
            url: str -> The target url from whom the reviews are to be extracted
            max_pages: int -> The no of pages to extract reviews from.
        Returns:
            quotes: List[Quote] t-> The extracted quotes from the website 
        """
        if max_pages == 0:
            return []
        
        quotes = []

        print(f"Starting to scrape url: {url}")
        scraped_result = await scrape_website(url)
        body_content = extract_body_content(scraped_result)
        cleaned_content = clean_body_content(body_content)
        chunks = chunk_content(cleaned_content, chunk_size=800)

        print(f"Passing content of {url} to llm")
        parsed_quotes = self.parse_quotes_with_llm(chunks)
        quotes.extend([quote_obj for list_of_quotes in parsed_quotes for quote_obj in list_of_quotes])

        print(f"Found quotes: {len(quotes)}")

        new_url = await self.get_url_with_pagination(url)

        paginated_results = await self.extract_quotes(url = new_url, max_pages = max_pages - 1)

        if paginated_results != []:
            quotes.extend(paginated_results)

        return quotes

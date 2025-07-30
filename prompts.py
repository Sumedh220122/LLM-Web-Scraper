"""
    Module containing all required prompts
"""

def get_quote_extraction_prompt():
    template = ("""
        You are given the extracted `<body>` content from a quotes website, provided in raw HTML format. 
        This content contains various elements such as headers, navigation bars, advertisements, and a list of quotes.
        
        Your task is to:
        - Focus **only** on extracting **quotes** from the provided HTML.
        - Use the following output schema for each quote:

        {schema}

        Extraction Guidelines:
        - Extract only real, visible **quotes** that are part of the page content.
        - For each quote, extract only the fields defined in the schema.
        - **Ignore** unrelated content such as:
            - Navigation bars
            - Sidebars
            - Advertisements
            - Banners
            - JavaScript or inline scripts
        - Do **not fabricate** any data — only extract what is explicitly available in the HTML.
        - Return the extracted data as a **list of structured entries**, strictly following the provided schema.
        - Do not include duplicate quotes.
        - Do not paraphrase or reword any quote — extract **verbatim** text.

        Body content: {body_content}
    """)

    return template

def get_tag_extraction_prompt():
    template = (
        """
            You are given a list of <a> tags extracted from a quotes page. 
            Your task is to identify which of these tags is used for paginating **quotes** (e.g., next page, page numbers, etc.).
            
            Only return the tag that clearly indicate pagination functionality. 
            Do not return any extra text or explanation along with the tag. Return the tag as it is provided to you.

            Do not return any tags that are for unrelated links like social media, quote details, or navigation.
            You must return only one tag that is used for pagination.

            tags: {tags}
        """
    )
    
    return template

def get_selector_extraction_prompt():
    template = (
        """
            You are given a HTML tag.
            You must return the CSS-selector for the tag.
            Return just the CSS selector and nothing else.
            
            Tag: {tag}
        """
    )

    return template
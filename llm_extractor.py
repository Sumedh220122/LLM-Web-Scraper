import os

from langchain_cohere import ChatCohere
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage


def extract(content: str, **kwargs):
    llm = ChatCohere(
            cohere_api_key = "")

    if 'schema_pydantic' in kwargs:
        schema = kwargs["schema_pydantic"]

        parser = PydanticOutputParser(pydantic_object=schema)

        template = (
            "Extract the following fields from the content:\n{format_instructions}\n"
            "Content:\n{content}"
        )
        prompt = PromptTemplate(
            input_variables=["query", "content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
            template=template,
        )

        product_query = "Give me the customer review details"

        try:
            chain = prompt | llm | parser
            
            response = chain.invoke({"query": product_query, "content" : content})

            return response
        except Exception as e:
            print(" ")

        return {}
    else:
        return {}

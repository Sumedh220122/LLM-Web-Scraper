# Website_scraping_using_LLM

The following project provides a tool for automating the process of web scraping by making use of LLM's.

The Description of the various .py files are as follows:
1. llm_extractor.py - makes use of the cohere llm in order to detect information pertaining to a structured schema.
   Documentation for the Cohere LLM is https://python.langchain.com/docs/integrations/providers/cohere/
2. scraping.py - uses playwright(a browser automation tool) to interact with the website to be scraped. The file also provides for functions to remove unwanted tags in the html structure of the document which makes it easy      for the llm to focus on important content
3. schema.py - defines the specific schema that is to be provided to the llm for information extraction.
4. main.py - main file running the extraction application

The application is deployed on a fast-api server.

# Usage

1. Install requirements by running pip install -r requirements.txt
2. Install playwright specific browsers by running playwright install in cmd
3. The following command is used to run the server in the command-prompt:
    ```
   uvicorn main:app --host 127.0.0.1 --port 5049 --log-level debug
   ```   
4. Paste the following url in the web-browser to access the appplication:
   ```
   http://localhost:5049/api/reviews/?url=?
   ```
   In place of ? paste the url of the website to be scraped.

# Examples
![image](https://github.com/user-attachments/assets/0580ccff-0dbe-4ba8-89a7-3776cf27606c)


Customer review extraction for the website - https://2717recovery.com/products/recovery-cream


 


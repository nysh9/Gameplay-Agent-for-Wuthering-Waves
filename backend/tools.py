import os
from firecrawl import Firecrawl
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

firecrawl_client = Firecrawl(api_key=("fc-cf822e9ebda34cb796c57fb9bb7939a2"))

@tool
def scrape_wuwa_build(character_name: str) -> str:
    """ß
    Finds the latest build, weapon, and echo recommendations for a Wuthering Waves character.
    Works with older Firecrawl Python SDK.
    """
    try:
        # Format name for URL
        name = character_name.lower().strip().replace(" ", "-")
        url = f"https://wuthering.gg/characters/{name}/"

        # Minimal call compatible with older SDK
        result = firecrawl_client.scrape(url)

        # Defensive: try to get Markdown
        markdown_content = getattr(result, "markdown", None)
        if not markdown_content:
            return f"Could not find build data for {character_name}."

        return markdown_content[:5000]

    except Exception as e:
        return f"Scraper Error: {str(e)}"

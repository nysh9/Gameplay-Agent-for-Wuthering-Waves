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


@tool
def get_farming_priority(union_level: int) -> str:
    """
    Provides farming recommendations based on player's Union Level.
    Use this when users ask what to farm or how to progress.
    """
    if union_level < 20:
        return """**Early Game (UL 1-19)**:
- Focus on story progression and world exploration
- Don't farm echoes yet - you'll replace them quickly
- Upgrade your highest rarity weapon to level 40"""
    
    elif union_level < 30:
        return """**Mid Game (UL 20-29)**:
- Start farming 3-star echoes with correct MAIN STATS (ATK%, Crit Rate/DMG)
- Substats don't matter yet
- Prioritize ascending your main DPS to level 60
- Clear Tactical Hologram for weapon materials"""
    
    elif union_level < 45:
        return """**Late Game (UL 30-44)**:
- Farm 4-star echo sets from Tacet Fields
- Build one full team (Main DPS + Sub DPS + Support)
- Start saving Astrite for limited banners
- Weekly bosses for character ascension materials"""
    
    else:
        return """**Endgame (UL 45+)**:
- Farm 5-star echo sets with optimized substats
- Prioritize Crit Rate/Crit DMG substats (aim for 1:2 ratio)
- Clear Tower of Adversity for premium rewards
- Farm weekly bosses for limited ascension materials"""
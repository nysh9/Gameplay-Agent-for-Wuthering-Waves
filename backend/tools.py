import os
import requests
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


GAME8_CHARACTER_IDS = {
    # SS Tier 1
    "shorekeeper": "463667",
    "cartethyia": "507777",
    "phrolova": "524877",
    "augusta": "524890",
    "iuno": "524889",
    "chisa": "524880",
    "lynae": "568211",
    "mornye": "568193",
    "aemeath": "572587",
    "sigrika": "568208",
    "hiyuki": "586421",
    # S Tier 1.5
    "verina": "454229",
    "jiyan": "454216",
    "carlotta": "486251",
    "phoebe": "486244",
    "brant": "486245",
    "cantarella": "500493",
    "zani": "486248",
    "ciaccona": "507924",
    "lupa": "520661",
    "galbrena": "524888",
    "qiuyuan": "524882",
    "luuk herssen": "568210",
    "denia": "585681",
    "sanhua": "454225",
    # A Tier 2
    "calcharo": "454217",
    "encore": "454221",
    "rover (spectro)": "454228",
    "rover (havoc)": "456120",
    "rover (aero)": "505267",
    "jinhsi": "455405",
    "changli": "452826",
    "zhezhi": "461497",
    "xiangli yao": "461501",
    "camellya": "473332",
    "roccia": "486246",
    "buling": "557981",
    "mortefi": "454222",
    "danjin": "454227",
    # B Tier 3
    "jianxin": "454213",
    "lingyang": "454223",
    "yinlin": "454218",
    "aalto": "454214",
    "yuanwu": "454219",
    "chixia": "454220",
    "baizhi": "454224",
    # C Tier 4
    "yangyang": "454215",
    "taoqi": "454226",
    "youhu": "463668",
    "lumi": "473488",
}


@tool
def get_reddit_meta(search_query: str) -> str:
    """Use this to find current community meta, team compositions, tier lists, or patch discussions from the Wuthering Waves subreddit. Use when asked about team comps, best characters, or current meta."""
    import re
    import html
    from urllib.parse import quote_plus
    import xml.etree.ElementTree as ET

    q = quote_plus(search_query)
    url = (
        f"https://www.reddit.com/r/WutheringWavesGuide/search.rss"
        f"?q={q}&restrict_sr=1&sort=top&t=month&limit=5"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0 Safari/537.36 WuwaAgent/1.0"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)[:3]

        if not entries:
            return f"No Reddit posts found for: {search_query}"

        chunks = []
        for e in entries:
            title_el = e.find("atom:title", ns)
            content_el = e.find("atom:content", ns)
            title = title_el.text if title_el is not None else ""
            raw_html = content_el.text if content_el is not None else ""
            # Strip HTML tags from content
            body = re.sub(r"<[^>]+>", "", html.unescape(raw_html or ""))
            body = re.sub(r"\s+", " ", body).strip()[:500]
            chunks.append(f"POST: {title}\n{body}\n---\n")

        return "".join(chunks)[:3000]
    except Exception as e:
        return f"Reddit error: {str(e)}"


@tool
def scrape_game8_guide(topic: str) -> str:
    """
    Scrapes Game8's Wuthering Waves wiki for tier lists,
    team compositions, and character guides. Use this for
    questions about: best characters, tier lists, team comps,
    who to pull, meta recommendations. Do NOT use for
    individual character builds — use scrape_wuwa_build for that.

    topic options: "tier_list", "best_teams", "character_{name}"
    """
    url_map = {
        "tier_list": "https://game8.co/games/Wuthering-Waves/archives/454729",
        "best_teams": "https://game8.co/games/Wuthering-Waves/archives/454728",
    }

    if topic.startswith("character_"):
        char = topic.replace("character_", "").lower().strip()
        char_id = GAME8_CHARACTER_IDS.get(char)
        if not char_id:
            return f"No Game8 page found for {char}"
        url = f"https://game8.co/games/Wuthering-Waves/archives/{char_id}"
    else:
        url = url_map.get(topic)
        if not url:
            return f"Unknown topic: {topic}"

    try:
        result = firecrawl_client.scrape(url)
        markdown_content = getattr(result, "markdown", None)
        if not markdown_content:
            return f"Could not scrape Game8 for topic: {topic}"

        # Skip Game8's membership / nav boilerplate by jumping to the article body.
        for marker in [
            "Wuthering Waves Walkthrough Team",
            "Last updated on",
            "Table of Contents",
        ]:
            idx = markdown_content.find(marker)
            if idx != -1:
                markdown_content = markdown_content[idx:]
                break

        return markdown_content[:12000]
    except Exception as e:
        return f"Scraper Error: {str(e)}"
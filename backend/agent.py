import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import scrape_wuwa_build, get_farming_priority

load_dotenv()


SYSTEM_PROMPT = """You are a Wuthering Waves build advisor. Your job is to give concise advice.

** Rules:**
1. NEVER dump raw wiki data. Extract only what the user needs.
2. ALWAYS ask for Union Level if recommendations depend on progression.
3. Keep responses under 150 words unless user asks for details.
4. Use bullet points for builds, prose for explanations.
5. If the scraped data is too long, summarize the TOP 3 most important points.

**Response Format:**
- For "Who should I pull?": Ask about their current roster and playstyle
- For "Best build for X?": Use scrape_wuwa_build, then extract: Best Weapon, Echo Set, Main Stats
- For "What should I farm?": Use get_farming_priority with their Union Level

**Personality:**
- Friendly but not overly casual
- Assume the user is competent but time-poor
- Proactively warn about common mistakes (e.g. "Don't level 10 characters at once")
"""

def create_wuwa_agent():
    """
    Initializes the agent with tools and LLM.
    
    Returns:
        CompiledStateGraph: Configured agent ready to handle queries
    """
    
    # Tools are already decorated with @tool in tools.py
    tools = [scrape_wuwa_build, get_farming_priority]
    
    # Create agent using the new LangGraph-based API
    # Pass model name as string, not ChatOpenAI object
    agent = create_agent(
        model="gpt-4o-mini",  # Model name as string
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        debug=True  # Shows reasoning steps like verbose=True
    )
    
    return agent
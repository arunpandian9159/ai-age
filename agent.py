import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List
from tripxplo_api import get_packages

# Load environment variables
load_dotenv(".env.local")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OpenRouter API key")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug log for API key and base URL
logger.info(f"Using OpenRouter API key: {OPENROUTER_API_KEY[:8]}... (masked)")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
logger.info(f"Using OpenRouter base URL: {OPENROUTER_BASE_URL}")

# Initialize OpenAI client with OpenRouter endpoint
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY
)

# LangGraph state class
class AgentState(BaseModel):
    messages: List[dict]

# DeepSeek call wrapper with logs
def call_deepseek(prompt: str) -> str:
    logger.info(f"Calling DeepSeek with prompt:\n{prompt}")
    try:
        res = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        content = res.choices[0].message.content or ""
        logger.info("Received response from DeepSeek")
        return content
    except Exception as e:
        logger.error(f"DeepSeek API error: {e}")
        return f"DeepSeek error: {e}"

# Core logic node for LangGraph
def query_node(state: AgentState) -> AgentState:
    user_query = state.messages[-1]["content"]
    logger.info(f"query_node received user query: {user_query}")

    packages = get_packages()
    logger.info(f"Fetched {len(packages)} packages from API")

    user_query_lower = user_query.lower()

    # Try to match destination keyword in package name/description
    matching_packages = [
        p for p in packages if user_query_lower in p.get("packageName", "").lower()
        or user_query_lower in p.get("description", "").lower()
    ]

    if matching_packages:
        logger.info(f"Found {len(matching_packages)} matching packages")

        # More structured list for better AI formatting
        formatted_list = "\n".join([
            f"{i+1}. {p.get('packageName', 'N/A')}\n"
            f"Duration: {p.get('noOfDays', 'N/A')}D/{p.get('noOfNight', 'N/A')}N\n"
            f"Starting From: ₹{p.get('startFrom', 'N/A')}\n"
            f"Package ID: {p.get('packageId', p.get('id', 'N/A'))}\n"
            for i, p in enumerate(matching_packages[:5])
        ])

        prompt = f"""
                    The user asked about a destination: {user_query}

                    Here are {len(matching_packages)} travel packages that match:

                    {formatted_list}

                    Now write a helpful travel description for the destination based on these packages.

                    ✅ Highlight each destination as a section.
                    ✅ List each package with:
                    - Name
                    - Duration
                    - Highlights
                    - Starting Price
                    - ❗ Always include "Package ID: xyz" as a clear line.
                    ✅ Be warm, friendly, and easy to understand.
                    ✅ Do NOT skip the Package IDs.
                    """
        response = call_deepseek(prompt)

    else:
        logger.info("No destination matches found. Falling back to general package list")

        general_list = "\n".join([
            f"{i+1}. {p.get('packageName', 'N/A')}\n"
            f"Duration: {p.get('noOfDays', 'N/A')}D/{p.get('noOfNight', 'N/A')}N\n"
            f"Starting From: ₹{p.get('startFrom', 'N/A')}\n"
            f"Package ID: {p.get('packageId', p.get('id', 'N/A'))}\n"
            for i, p in enumerate(packages[:5])
        ])

        prompt = f"""
                    The user asked: {user_query}

                    Here are some of our most popular packages:

                    {general_list}

                    Format them nicely for a general travel recommendation.

                    ✅ Show duration, starting price, and Package ID clearly.
                    ✅ Keep the tone inviting and helpful.
                    """
        response = call_deepseek(prompt)

    logger.info("Appending assistant response to state messages")
    state.messages.append({"role": "assistant", "content": response})
    return state

# LangGraph setup
def build_graph():
    logger.info("Building StateGraph for agent")
    builder = StateGraph(AgentState)
    builder.add_node("query_node", query_node)
    builder.set_entry_point("query_node")
    builder.set_finish_point("query_node")
    compiled_graph = builder.compile()
    logger.info("StateGraph compiled successfully")
    return compiled_graph

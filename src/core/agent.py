import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List
from ..services.tripxplo_api import get_packages, get_available_hotels, get_available_vehicles, get_available_activities

# Load environment variables from .env.local
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env.local'))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OpenRouter API key")

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

class AgentState(BaseModel):
    messages: List[dict]

def call_deepseek(prompt: str) -> str:
    logger.info("Calling DeepSeek API")
    try:
        res = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        logger.info("Received response from DeepSeek")
        content = res.choices[0].message.content
        return content if content is not None else ""
    except Exception as e:
        logger.error(f"DeepSeek API error: {e}")
        return f"DeepSeek error: {e}"

def extract_search_terms(query: str) -> str:
    known_destinations = [
        "goa", "kerala", "manali", "bali", "kodaikanal", "ooty",
        "rajasthan", "andaman", "himachal", "shimla", "darjeeling"
    ]
    query_lower = query.lower()
    found_terms = [dest for dest in known_destinations if dest in query_lower]
    if found_terms:
        logger.info(f"Extracted search terms: {found_terms}")
        return " ".join(found_terms)
    logger.info("No known destinations found in query; using full query as search term")
    return query

def detect_intent(query: str) -> str:
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in ["hotel", "stay", "accommodation", "resort"]):
        return "hotel"
    if any(keyword in query_lower for keyword in ["vehicle", "car", "transport", "taxi"]):
        return "vehicle"
    if any(keyword in query_lower for keyword in ["activity", "tour", "things to do", "adventure", "experience"]):
        return "activity"
    return "package"

def format_packages(packages: list) -> str:
    return "\n".join([
        f"{i+1}. {p.get('packageName', 'N/A')} (ID: {p.get('packageId', p.get('id', 'N/A'))})"
        for i, p in enumerate(packages[:5])
    ])

def query_node(state: AgentState) -> AgentState:
    user_query = state.messages[-1]["content"].strip()
    logger.info(f"Received user query (length {len(user_query)} chars)")

    if len(user_query) < 5:
        clarification = (
            "Hi! Your query seems a bit short. Could you please provide more details? "
            "For example, mention the destination, type of package, or any preferences."
        )
        state.messages.append({"role": "assistant", "content": clarification})
        return state

    intent = detect_intent(user_query)
    logger.info(f"Detected intent: {intent}")

    search_term = extract_search_terms(user_query)

    if intent == "hotel":
        logger.info(f"Fetching hotels with search term '{search_term}'")
        hotels = get_available_hotels(search_term)
        if hotels:
            formatted_list = "\n".join([
                f"{i+1}. {h.get('hotelName', 'N/A')} (ID: {h.get('hotelId', 'N/A')})"
                for i, h in enumerate(hotels[:5])
            ])
            prompt = f"""
You are a helpful travel assistant.

The user asked about hotels: "{user_query}"

Here are some hotel options matching your request:

{formatted_list}

Please provide a warm, clear, and friendly summary for these hotel options including name, highlights, price (if available), and Hotel ID.

End with a call to action encouraging booking or further questions.
"""
            response = call_deepseek(prompt)
        else:
            response = "Sorry, I couldn't find hotels matching your request. Would you like me to suggest popular hotels instead?"

    elif intent == "vehicle":
        logger.info(f"Fetching vehicles with search term '{search_term}'")
        vehicles = get_available_vehicles(search_term)
        if vehicles:
            formatted_list = "\n".join([
                f"{i+1}. {v.get('vehicleName', 'N/A')} (ID: {v.get('vehicleId', 'N/A')})"
                for i, v in enumerate(vehicles[:5])
            ])
            prompt = f"""
You are a helpful travel assistant.

The user asked about vehicles: "{user_query}"

Here are some vehicle options matching your request:

{formatted_list}

Please provide a friendly summary for these vehicles including name, type, price (if available), and Vehicle ID.

End with a call to action encouraging booking or further questions.
"""
            response = call_deepseek(prompt)
        else:
            response = "Sorry, I couldn't find vehicles matching your request. Would you like me to suggest popular vehicles instead?"

    elif intent == "activity":
        logger.info(f"Fetching activities with search term '{search_term}'")
        activities = get_available_activities(search_term)
        if activities:
            formatted_list = "\n".join([
                f"{i+1}. {a.get('activityName', 'N/A')} (ID: {a.get('activityId', 'N/A')})"
                for i, a in enumerate(activities[:5])
            ])
            prompt = f"""
                        You are a helpful travel assistant.

                        The user asked about activities: "{user_query}"

                        Here are some activity options matching your request:

                        {formatted_list}

                        Please provide a warm, engaging summary for these activities including name, highlights, price (if available), and Activity ID.

                        End with a call to action encouraging booking or further questions.
                        """
            response = call_deepseek(prompt)
        else:
            response = "Sorry, I couldn't find activities matching your request. Would you like me to suggest popular activities instead?"

    else:  # Default to package search
        logger.info(f"Fetching packages with search term '{search_term}'")
        packages = get_packages()
        logger.info(f"Number of packages fetched: {len(packages)}")
        if packages:
            formatted_list = format_packages(packages)
            prompt = f"""
                        You are a helpful travel assistant.

                        The user asked about packages: "{user_query}"

                        Step-by-step:

                        1. Identify the main destination or theme.
                        2. Find the best matches from the packages below.
                        3. Summarize each package with name, duration, highlights, price, and Package ID.
                        4. Present warmly and clearly, grouped by destination if applicable.
                        5. End with a friendly call to action.

                        Here are the matching packages ({len(packages)} found):

                        {formatted_list}
                        """
            response = call_deepseek(prompt)
        else:
            logger.info("No packages matched; providing popular packages")
            general_packages = get_packages()
            formatted_list = format_packages(general_packages)
            prompt = f"""
                        You are a helpful travel assistant.

                        The user asked: "{user_query}"

                        We couldn't find exact matches, but here are some popular travel packages:

                        {formatted_list}

                        Please format this as a friendly, inviting travel recommendation showing duration, price, and Package ID clearly.
                        """
            response = call_deepseek(prompt)

    state.messages.append({"role": "assistant", "content": response})
    return state

def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("query_node", query_node)
    builder.set_entry_point("query_node")
    builder.set_finish_point("query_node")
    logger.info("Graph built successfully")
    return builder.compile()
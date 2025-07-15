import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.core.agent import build_graph
from src.services.tripxplo_api import (
    get_packages, get_package_details, get_package_pricing,
    get_available_hotels, get_available_vehicles, get_available_activities
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
graph = build_graph()

# CORS settings for dev - open to all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "TripXplo AI API — POST /query with {'question': 'your query'}"}

@app.post("/query")
async def run_agent(request: QueryRequest):
    user_input = request.question
    logger.info(f"Received query: {user_input}")

    state = {"messages": [{"role": "user", "content": user_input}]}
    logger.info("Invoking AI graph with user input")

    try:
        result = graph.invoke(state)
        logger.info("AI graph invocation successful")

        response_text = result["messages"][-1]["content"]
        logger.info(f"AI response generated: {response_text}")

        return {"response": response_text}

    except Exception as e:
        logger.error(f"Error during AI invocation: {e}")
        return {"error": "Something went wrong while processing your query."}

@app.get("/packages")
async def fetch_packages():
    logger.info("API call: get_packages()")
    packages = get_packages()
    logger.info(f"get_packages() returned {len(packages)} packages")
    return {"packages": packages}

@app.get("/packages/{package_id}")
async def fetch_package_details(package_id: str):
    logger.info(f"API call: get_package_details({package_id})")
    details = get_package_details(package_id)
    logger.info(f"get_package_details({package_id}) returned data")
    return details

@app.get("/packages/{package_id}/pricing")
async def fetch_package_pricing(
    package_id: str,
    startDate: str,
    noAdult: int,
    noChild: int,
    noRoomCount: int,
    noExtraAdult: int = 0
):
    logger.info(f"API call: get_package_pricing({package_id}, startDate={startDate}, noAdult={noAdult}, noChild={noChild}, noRoomCount={noRoomCount}, noExtraAdult={noExtraAdult})")
    pricing = get_package_pricing(package_id, {
        "startDate": startDate,
        "noAdult": noAdult,
        "noChild": noChild,
        "noRoomCount": noRoomCount,
        "noExtraAdult": noExtraAdult
    })
    logger.info(f"get_package_pricing({package_id}) returned pricing data")
    return pricing

@app.get("/packages/{package_id}/hotels")
async def fetch_hotels(package_id: str):
    logger.info(f"API call: get_available_hotels({package_id})")
    hotels = get_available_hotels(package_id)
    logger.info(f"get_available_hotels({package_id}) returned {len(hotels)} hotels")
    return {"hotels": hotels}

@app.get("/packages/{package_id}/vehicles")
async def fetch_vehicles(package_id: str):
    logger.info(f"API call: get_available_vehicles({package_id})")
    vehicles = get_available_vehicles(package_id)
    logger.info(f"get_available_vehicles({package_id}) returned {len(vehicles)} vehicles")
    return {"vehicles": vehicles}

@app.get("/packages/{package_id}/activities")
async def fetch_activities(package_id: str):
    logger.info(f"API call: get_available_activities({package_id})")
    activities = get_available_activities(package_id)
    logger.info(f"get_available_activities({package_id}) returned {len(activities)} activities")
    return {"activities": activities}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.agent import AgentState, query_node
from src.services.tripxplo_api import (
    get_packages, get_package_details, get_package_pricing,
    get_available_hotels, get_available_vehicles, get_available_activities
)
from src.models.schemas import QueryRequest, QueryResponse
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered travel planning assistant for TripXplo"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TripXplo AI API — POST /query with {'question': 'your query'}"}

@app.post("/query", response_model=QueryResponse)
async def run_agent(request: QueryRequest):
    user_input = request.question
    logger.info(f"Received query: {user_input}")

    try:
        # Initialize state with user input
        state = AgentState(messages=[{"role": "user", "content": user_input}])
        
        # Process query directly
        result = query_node(state)
        logger.info("Query processing successful")
        
        # Get response from the last message
        response_text = result.messages[-1]["content"]
        logger.info(f"AI response generated: {response_text}")
        
        return QueryResponse(response=response_text)

    except Exception as e:
        import traceback
        logger.error(f"Error during query processing: {e}")
        logger.error(traceback.format_exc())
        return QueryResponse(response="", error=f"Error: {str(e)}")

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

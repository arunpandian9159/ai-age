import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv(".env.local")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API = "https://api.tripxplo.com/v1/api"
EMAIL = os.getenv("TRIPXPLO_EMAIL")
PASSWORD = os.getenv("TRIPXPLO_PASSWORD")

TOKEN = None

def get_token():
    global TOKEN
    if TOKEN:
        logger.info("Using cached token")
        return TOKEN

    logger.info("Requesting new token from TripXplo API")
    try:
        res = requests.put(f"{API}/admin/auth/login", json={"email": EMAIL, "password": PASSWORD})
        res.raise_for_status()
        TOKEN = res.json().get("accessToken")
        if not TOKEN:
            logger.error("No accessToken found in login response")
            raise ValueError("Failed to get accessToken")
        logger.info("Token retrieved successfully")
        return TOKEN
    except requests.RequestException as e:
        logger.error(f"HTTP error during token fetch: {e}")
        raise
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        raise

def get_packages():
    token = get_token()
    logger.info("Fetching packages from TripXplo API")
    try:
        res = requests.get(
            f"{API}/admin/package?limit=50&offset=0",
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        packages = res.json().get("result", {}).get("docs", [])
        logger.info(f"Fetched {len(packages)} packages")
        return packages
    except requests.RequestException as e:
        logger.error(f"HTTP error during packages fetch: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during packages fetch: {e}")
        return []

def get_package_details(package_id):
    token = get_token()
    logger.info(f"Fetching details for package_id={package_id}")
    try:
        res = requests.get(
            f"{API}/admin/package/{package_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        details = res.json().get("result", {})
        logger.info(f"Fetched package details for {package_id}")
        return details
    except requests.RequestException as e:
        logger.error(f"HTTP error during package details fetch: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error during package details fetch: {e}")
        return {}

def get_package_pricing(package_id, params):
    token = get_token()
    logger.info(f"Fetching pricing for package_id={package_id} with params={params}")
    try:
        res = requests.post(
            f"{API}/admin/package/{package_id}/pricing",
            json=params,
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        pricing = res.json().get("result", {})
        logger.info(f"Fetched pricing for package {package_id}")
        return pricing
    except requests.RequestException as e:
        logger.error(f"HTTP error during package pricing fetch: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error during package pricing fetch: {e}")
        return {}

def get_available_hotels(package_id):
    token = get_token()
    logger.info(f"Fetching available hotels for package_id={package_id}")
    try:
        res = requests.get(
            f"{API}/admin/package/{package_id}/hotels",
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        hotels = res.json().get("result", [])
        logger.info(f"Fetched {len(hotels)} hotels for package {package_id}")
        return hotels
    except requests.RequestException as e:
        logger.error(f"HTTP error during hotels fetch: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during hotels fetch: {e}")
        return []

def get_available_vehicles(package_id):
    token = get_token()
    logger.info(f"Fetching available vehicles for package_id={package_id}")
    try:
        res = requests.get(
            f"{API}/admin/package/{package_id}/vehicles",
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        vehicles = res.json().get("result", [])
        logger.info(f"Fetched {len(vehicles)} vehicles for package {package_id}")
        return vehicles
    except requests.RequestException as e:
        logger.error(f"HTTP error during vehicles fetch: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during vehicles fetch: {e}")
        return []

def get_available_activities(package_id):
    token = get_token()
    logger.info(f"Fetching available activities for package_id={package_id}")
    try:
        res = requests.get(
            f"{API}/admin/package/{package_id}/activities",
            headers={"Authorization": f"Bearer {token}"}
        )
        res.raise_for_status()
        activities = res.json().get("result", [])
        logger.info(f"Fetched {len(activities)} activities for package {package_id}")
        return activities
    except requests.RequestException as e:
        logger.error(f"HTTP error during activities fetch: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during activities fetch: {e}")
        return []

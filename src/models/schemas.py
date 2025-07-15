from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    response: str
    error: Optional[str] = None

class PackageBase(BaseModel):
    packageId: str
    packageName: str
    noOfDays: int
    noOfNight: int
    startFrom: float
    description: Optional[str] = None

class PackageDetails(PackageBase):
    itinerary: Optional[List[Dict[str, Any]]] = None
    inclusions: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    terms: Optional[str] = None

class PricingRequest(BaseModel):
    startDate: str
    noAdult: int
    noChild: int
    noRoomCount: int
    noExtraAdult: int = 0

class PricingResponse(BaseModel):
    totalPrice: float
    breakdown: Optional[Dict[str, Any]] = None

class Hotel(BaseModel):
    hotelId: str
    hotelName: str
    location: str
    rating: Optional[float] = None
    price: Optional[float] = None

class Vehicle(BaseModel):
    vehicleId: str
    vehicleName: str
    vehicleType: str
    capacity: int
    price: Optional[float] = None

class Activity(BaseModel):
    activityId: str
    activityName: str
    description: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[float] = None
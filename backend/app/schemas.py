from pydantic import BaseModel, Field
from typing import Optional

class CarFeatures(BaseModel):
    company: str
    model: str
    edition: Optional[str] = None
    year: int = Field(ge=1990, le=2026)
    owner: Optional[str] = None  # "First", "Second", "Third", etc.
    fuel: str
    seller_type: str
    transmission: str
    km_driven: float
    mileage_mpg: Optional[float] = None
    engine_cc: float
    max_power_bhp: float
    torque_nm: Optional[float] = None

class PredictionResponse(BaseModel):
    price_mad: float

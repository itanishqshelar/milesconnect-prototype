"""
FastAPI ML Service

Provides REST API endpoints for ML predictions:
- Driver performance scoring
- Predictive maintenance
- Demand forecasting
- Delivery performance analytics
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from models.driver_scoring import DriverScoringModel
from models.maintenance_prediction import MaintenancePredictionModel
from models.demand_forecast import DemandForecastModel

# Initialize FastAPI app
app = FastAPI(
    title="MilesConnect ML Service",
    description="Machine Learning service for predictive analytics in logistics",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models
model_dir = Path(__file__).parent.parent.parent / "models"
driver_model = DriverScoringModel()
maintenance_model = MaintenancePredictionModel()
demand_model = DemandForecastModel()

# Try to load models (they need to be trained first)
try:
    driver_model.load(model_dir)
    print("✓ Driver scoring model loaded")
except Exception as e:
    print(f"⚠ Driver scoring model not loaded: {e}")

try:
    maintenance_model.load(model_dir)
    print("✓ Maintenance prediction model loaded")
except Exception as e:
    print(f"⚠ Maintenance prediction model not loaded: {e}")

try:
    demand_model.load(model_dir)
    print("✓ Demand forecast model loaded")
except Exception as e:
    print(f"⚠ Demand forecast model not loaded: {e}")


# Pydantic models for request/response
class DriverData(BaseModel):
    driver_id: Optional[str] = None
    total_trips: int
    on_time_deliveries: int
    late_deliveries: int
    avg_speed_kmh: float
    harsh_braking_count: int
    harsh_acceleration_count: int
    idle_time_mins: float
    fuel_efficiency_kmpl: float
    distance_km: float
    experience_months: int
    incident_count: int
    customer_rating: float


class DriverScoreResponse(BaseModel):
    driver_id: Optional[str]
    score: float
    metrics: Dict[str, float]


class VehicleData(BaseModel):
    vehicle_id: Optional[str] = None
    age_months: int
    odometer_km: int
    days_since_last_maintenance: int
    total_trips: int
    avg_trip_distance_km: float
    harsh_usage_score: float
    fuel_consumption_variance: float
    reported_issues_count: int


class MaintenancePredictionResponse(BaseModel):
    vehicle_id: Optional[str]
    predicted_class: str
    confidence: float
    days_until_maintenance: int
    class_probabilities: Dict[str, float]


class DemandForecastData(BaseModel):
    day_of_week: int
    month: int
    is_holiday: bool
    historical_shipments_7d: int
    historical_shipments_30d: int
    avg_shipment_weight_kg: float
    active_vehicles_count: int
    seasonal_index: float


class DemandForecastResponse(BaseModel):
    predicted_shipments: int
    forecast_7d: Optional[List[Dict[str, int]]] = None


# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MilesConnect ML Service",
        "models": {
            "driver_scoring": driver_model.model is not None,
            "maintenance_prediction": maintenance_model.model is not None,
            "demand_forecast": demand_model.model is not None
        }
    }


@app.post("/api/ml/driver-score", response_model=DriverScoreResponse)
async def calculate_driver_score(data: DriverData):
    """Calculate driver performance score"""
    try:
        if driver_model.model is None:
            raise HTTPException(status_code=503, detail="Driver scoring model not available")
        
        # Convert to dict
        driver_dict = data.dict()
        
        # Predict score
        score = driver_model.predict(driver_dict)[0]
        
        # Calculate individual metrics
        on_time_rate = data.on_time_deliveries / (data.total_trips + 1)
        safety_events = data.harsh_braking_count + data.harsh_acceleration_count
        safety_score = max(0, 100 - (safety_events / (data.total_trips + 1)) * 50)
        
        return DriverScoreResponse(
            driver_id=data.driver_id,
            score=round(score, 2),
            metrics={
                "on_time_delivery_rate": round(on_time_rate * 100, 2),
                "fuel_efficiency_kmpl": round(data.fuel_efficiency_kmpl, 2),
                "safety_score": round(safety_score, 2),
                "customer_rating": round(data.customer_rating, 2),
                "experience_months": data.experience_months
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ml/maintenance-prediction", response_model=MaintenancePredictionResponse)
async def predict_maintenance(data: VehicleData):
    """Predict vehicle maintenance needs"""
    try:
        if maintenance_model.model is None:
            raise HTTPException(status_code=503, detail="Maintenance prediction model not available")
        
        # Convert to dict
        vehicle_dict = data.dict()
        
        # Predict
        result = maintenance_model.predict(vehicle_dict)[0]
        
        return MaintenancePredictionResponse(
            vehicle_id=data.vehicle_id,
            predicted_class=result['predicted_class'],
            confidence=round(result['confidence'], 4),
            days_until_maintenance=result['days_until_maintenance'],
            class_probabilities=result['class_probabilities']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ml/demand-forecast", response_model=DemandForecastResponse)
async def forecast_demand(data: DemandForecastData):
    """Forecast shipment demand"""
    try:
        if demand_model.model is None:
            raise HTTPException(status_code=503, detail="Demand forecast model not available")
        
        # Convert to dict
        forecast_dict = data.dict()
        
        # Predict next day
        prediction = demand_model.predict(forecast_dict)[0]
        
        # Also get 7-day forecast
        forecast_7d = demand_model.forecast_next_n_days(forecast_dict, n_days=7)
        
        return DemandForecastResponse(
            predicted_shipments=int(prediction),
            forecast_7d=forecast_7d
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ml/driver-score/batch")
async def calculate_driver_scores_batch(drivers: List[DriverData]):
    """Calculate scores for multiple drivers"""
    try:
        if driver_model.model is None:
            raise HTTPException(status_code=503, detail="Driver scoring model not available")
        
        results = []
        for driver in drivers:
            score = driver_model.predict(driver.dict())[0]
            on_time_rate = driver.on_time_deliveries / (driver.total_trips + 1)
            safety_events = driver.harsh_braking_count + driver.harsh_acceleration_count
            safety_score = max(0, 100 - (safety_events / (driver.total_trips + 1)) * 50)
            
            results.append({
                "driver_id": driver.driver_id,
                "score": round(score, 2),
                "metrics": {
                    "on_time_delivery_rate": round(on_time_rate * 100, 2),
                    "fuel_efficiency_kmpl": round(driver.fuel_efficiency_kmpl, 2),
                    "safety_score": round(safety_score, 2),
                    "customer_rating": round(driver.customer_rating, 2)
                }
            })
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {"drivers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

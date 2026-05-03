from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.forecast import router as forecast_router
from api.optimize import router as optimize_router
app = FastAPI(
    title="SMMS ML Backend",
    description="Standalone API for Smart Mess Management System (SMMS) Machine Learning insights",
    version="1.0.0"
)

# Configure CORS to accept requests from the Flutter client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to match your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(forecast_router, prefix="/api/v1/forecast", tags=["Forecast"])
app.include_router(optimize_router, prefix="/api/v1/optimize", tags=["Optimization"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SMMS ML Backend API"}

from fastapi import FastAPI
from backend.routes.disaster_routes import router as disaster_router
from backend.routes.prediction_routes import router as prediction_router

app = FastAPI()

# Include routers
app.include_router(disaster_router, prefix="/disasters")
app.include_router(prediction_router, prefix="/predictions")

@app.get("/")
def home():
    return {"message": "Disaster Prediction System API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

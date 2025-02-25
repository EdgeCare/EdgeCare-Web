from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import edgecare
import uvicorn

# App setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only the frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EdgeCare Web server is running!"}

# Include routes
app.include_router(edgecare.router, prefix="/edgecare", tags=["EdgeCare"])

if __name__ == "__main__":

    # FAST API server
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)

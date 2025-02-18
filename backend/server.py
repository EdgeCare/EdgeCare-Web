from fastapi import FastAPI, HTTPException, Depends
from routes import edgecare
import uvicorn

# App setup
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "EdgeCare server is running!"}

# Include routes
app.include_router(edgecare.router, prefix="/edgecare", tags=["EdgeCare"])

if __name__ == "__main__":

    # FAST API server
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
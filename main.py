import uvicorn
from fastapi import FastAPI
from routes import auth, profile

# Initialize FastAPI 
app = FastAPI(
    title="User Account Management Service",
    version="1.0.0",
    docs_url="/",
    description="Microservice for managing user accounts",
    swagger_ui_init_oauth={"usePkceWithAuthorizationCodeGrant": True},
    openapi_tags=[{"name": "User", "description": "Operations related to user management"}]
)

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/health", tags=["User"])
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware  # Added for CORS
from pydantic import BaseModel, constr
import os
from dotenv import load_dotenv
from google.generativeai import configure
from agents.tutor_agent import tutor_agent
import logging  # Added for logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables and configure Gemini API
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tutor-agent-system.vercel.app/",  # Replace with your Vercel URL
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware (optional but recommended)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic model for request body
class Query(BaseModel):
    query: constr(min_length=1)  # Ensures query is not empty

# Web Interface
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Serves the web interface for the Tutor Agent application.
    
    Args:
        request (Request): The HTTP request object.
    
    Returns:
        TemplateResponse: Rendered index.html template.
    """
    logger.info("Serving index.html")
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoint
@app.post("/api/query")
async def query_endpoint(query: Query):
    """
    Handles API requests to process user queries via the Tutor Agent.
    
    Args:
        query (Query): Pydantic model containing the user query.
    
    Returns:
        dict: JSON response with the agent's response or an error message.
    """
    try:
        logger.info(f"Received query: {query.query}")
        response = tutor_agent(query.query)
        logger.info(f"Generated response: {response}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {"error": f"Internal server error: {str(e)}"}

# Health Check Endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status of the API.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
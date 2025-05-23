from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, constr
import os
from dotenv import load_dotenv
from google.generativeai import configure
from agents.tutor_agent import tutor_agent

# Load environment variables and configure Gemini API
load_dotenv()
configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()
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
        response = tutor_agent(query.query)
        return {"response": response}
    except Exception as e:
        return {"error": f"Internal server error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
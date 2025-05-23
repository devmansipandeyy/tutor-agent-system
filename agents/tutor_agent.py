import re
from google.generativeai import GenerativeModel
from agents.math_agent import math_agent
from agents.physics_agent import physics_agent
from tools.physics_tools import physics_constants

def tutor_agent(query: str) -> str:
    """
    Routes user queries to appropriate sub-agents (Math, Physics) or Gemini API directly.
    
    Args:
        query (str): User query (e.g., "Solve 2x + 5 = 11").
    
    Returns:
        str: Response from the appropriate agent or Gemini API.
    """
    lower_query = query.lower()
    
    # Route to Math Agent if query contains math-related keywords or arithmetic
    if "math" in lower_query or re.search(r"\d+\s*[\+\-\*/]\s*\d+", lower_query) or "equation" in lower_query or "solve" in lower_query:
        return math_agent(query)
    
    # Route to Physics Agent if query contains physics-related keywords or constants
    all_constants = list(physics_constants.keys())
    if "physics" in lower_query or "newton" in lower_query or "force" in lower_query or any(key in lower_query for key in all_constants):
        return physics_agent(query)
    
    # Default to Gemini API for general queries
    prompt = f"Provide a clear and concise answer to the query: '{query}'"
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
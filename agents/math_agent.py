import re
from google.generativeai import GenerativeModel
from tools.math_tools import calculator

def math_agent(query: str) -> str:
    """
    Handles math-related queries, using the calculator tool for arithmetic and Gemini API for explanations.
    
    Args:
        query (str): User query (e.g., "Solve 2x + 5 = 11").
    
    Returns:
        str: Response with explanation and result (if applicable).
    """
    # Regex to detect arithmetic expressions (e.g., 2 + 3, 5 * 4)
    calc_regex = r"\d+\s*[\+\-\*/]\s*\d+"
    match = re.search(calc_regex, query)
    model = GenerativeModel("gemini-1.5-flash")
    
    if match:
        result = calculator(match.group(0))
        prompt = f"Explain the solution to the math query: '{query}'. The calculation result is {result}."
        response = model.generate_content(prompt)
        return f"{response.text}\nResult: {result}"
    else:
        prompt = f"Provide a clear and concise explanation for the math query: '{query}'"
        response = model.generate_content(prompt)
        return response.text
from google.generativeai import GenerativeModel
from tools.physics_tools import physics_constants, lookup_constant

def physics_agent(query: str) -> str:
    """
    Handles physics-related queries, using the constants lookup tool and Gemini API for explanations.
    
    Args:
        query (str): User query (e.g., "What is the speed of light?").
    
    Returns:
        str: Response with explanation and constant value (if applicable).
    """
    lower_query = query.lower()
    model = GenerativeModel("gemini-1.5-flash")
    
    # Check for constants in the JSON file
    all_constants = list(physics_constants.keys())
    found_constant = None
    for key in all_constants:
        if key in lower_query:
            found_constant = key
            break

    if found_constant:
        constant_value = lookup_constant(found_constant)
        if "Constant not found" in constant_value:
            prompt = f"Explain the physics concept related to '{found_constant}' in the query: '{query}'. Note that the constant value could not be retrieved."
            response = model.generate_content(prompt)
            return f"{response.text}\nNote: {constant_value}"
        else:
            prompt = f"Explain the significance of the {found_constant} in the context of the query: '{query}'. Its value is {constant_value}."
            response = model.generate_content(prompt)
            return f"{response.text}\nValue: {constant_value}"
    
    # Handle general physics queries
    prompt = f"Provide a clear and concise explanation for the physics query: '{query}'"
    response = model.generate_content(prompt)
    return response.text
import json
from pathlib import Path

# Load physics constants from JSON file
CONSTANTS_PATH = Path(__file__).parent / "physics_constants.json"
try:
    with open(CONSTANTS_PATH, 'r') as f:
        physics_constants = json.load(f)
except FileNotFoundError:
    physics_constants = {}

def lookup_constant(constant_name: str) -> str:
    """
    Looks up a physical constant by name from a JSON file.
    
    Args:
        constant_name (str): Name of the constant (e.g., "speed of light").
    
    Returns:
        str: Formatted string with the constant's value, unit, and uncertainty (if available).
    """
    lower_name = constant_name.lower()

    # Check constants from JSON
    if lower_name in physics_constants:
        const_data = physics_constants[lower_name]
        return f"{const_data['value']} {const_data['unit']} (uncertainty: {const_data['uncertainty']})"

    return "Constant not found"
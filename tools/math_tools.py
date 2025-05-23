def calculator(expression: str) -> str:
    """
    Evaluates a basic arithmetic expression safely and returns the result as a string.
    
    Args:
        expression (str): Arithmetic expression (e.g., "2 + 3").
    
    Returns:
        str: Result of the calculation or an error message.
    """
    try:
        # Safe eval for basic arithmetic
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result) if isinstance(result, (int, float)) else "Invalid calculation"
    except Exception:
        return "Error in calculation"

from typing import Tuple, Any, List, Union, Dict

__all__ = ["get_parameters"]

def get_parameters(request, parameters: List[str]) -> bool:
    try:
        data = request.get_json()
    except:
        return None
    for param in parameters:
        if param not in data:
            return None
    return data
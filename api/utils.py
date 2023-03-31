from typing import Tuple, Any, List, Union, Dict

__all__ = ["check_parameters"]

def check_parameters(data: Dict, parameters: List[str]) -> bool:
    for param in parameters:
        if param not in data:
            return False
    return True
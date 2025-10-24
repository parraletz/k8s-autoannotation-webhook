"""
Validator service
"""


def require(condition: bool, message: str) -> None:
    """
    Raises a ValueError if the condition is not met
    """
    if not condition:
        raise ValueError(message)

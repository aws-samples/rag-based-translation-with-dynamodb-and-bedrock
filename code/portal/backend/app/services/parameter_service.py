from typing import List, Dict, Any, Optional
from app.services.aws_service import aws_service

async def get_parameters_by_path(path: str) -> List[Dict[str, Any]]:
    """
    Get parameters from Parameter Store by path
    """
    return await aws_service.get_parameters_by_path(path)

async def update_parameter(name: str, value: str) -> bool:
    """
    Update a parameter in Parameter Store
    """
    return await aws_service.update_parameter(name, value)

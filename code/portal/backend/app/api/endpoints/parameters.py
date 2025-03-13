from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.models.user import User
from app.api.dependencies.auth import check_super_admin_permission
from app.services.parameter_service import get_parameters_by_path, update_parameter

router = APIRouter()

@router.get("/by-path/{path:path}")
async def get_parameters_by_path_endpoint(
    path: str,
    current_user: User = Depends(check_super_admin_permission)
):
    """
    Get parameters from Parameter Store by path
    """
    try:
        parameters = await get_parameters_by_path(path)
        return {"parameters": parameters}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get parameters: {str(e)}"
        )

@router.put("/{name:path}")
async def update_parameter_endpoint(
    name: str,
    value: str,
    current_user: User = Depends(check_super_admin_permission)
):
    """
    Update a parameter in Parameter Store
    """
    try:
        success = await update_parameter(name, value)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update parameter: {name}"
            )
        return {"message": f"Parameter {name} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update parameter: {str(e)}"
        )

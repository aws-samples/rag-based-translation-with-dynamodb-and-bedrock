from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from fastapi.responses import JSONResponse
import json
from typing import List, Dict, Any, Optional

from app.models.dictionary import DictionaryTerm, DictionaryTermUpdate, DictionaryVersion, DictionaryVersionUpdate, DictionaryQualityCheck
from app.models.user import User
from app.api.dependencies.auth import get_current_active_user, check_admin_permission
from app.services.dictionary_service import (
    list_dictionaries, get_dictionaries_with_versions, get_current_version,
    update_current_version, query_term, update_term_mapping, upload_dictionary,
    check_dictionary_job_status, term_mapping_quality_check
)

router = APIRouter()

@router.get("/list")
async def list_dictionaries_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """
    List all dictionaries
    """
    try:
        dictionaries = await list_dictionaries()
        return {"dictionaries": dictionaries or ["default_dictionary"]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list dictionaries: {str(e)}"
        )

@router.get("/versions")
async def get_dictionary_versions(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get dictionaries with their versions
    """
    try:
        dict_versions = await get_dictionaries_with_versions()
        return {"dictionary_versions": dict_versions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dictionary versions: {str(e)}"
        )

@router.get("/current-version/{dict_id}")
async def get_dictionary_current_version(
    dict_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current version of a dictionary
    """
    try:
        version = await get_current_version(dict_id)
        return {"dict_id": dict_id, "current_version": version}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current version: {str(e)}"
        )

@router.put("/current-version/{dict_id}")
async def update_dictionary_current_version(
    dict_id: str,
    version_update: DictionaryVersionUpdate,
    current_user: User = Depends(check_admin_permission)
):
    """
    Update the current version of a dictionary
    """
    try:
        await update_current_version(dict_id, version_update.version)
        return {"message": f"Updated current version of {dict_id} to {version_update.version}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update current version: {str(e)}"
        )

@router.get("/term/{dictionary_name}/{term}")
async def get_dictionary_term(
    dictionary_name: str,
    term: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Query a term from a dictionary
    """
    try:
        term_data = await query_term(dictionary_name, term)
        if term_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Term '{term}' not found in dictionary '{dictionary_name}'"
            )
        return term_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query term: {str(e)}"
        )

@router.put("/term/{dictionary_name}/{term}")
async def update_dictionary_term(
    dictionary_name: str,
    term: str,
    term_update: DictionaryTermUpdate,
    current_user: User = Depends(check_admin_permission)
):
    """
    Update a term mapping in a dictionary
    """
    try:
        await update_term_mapping(
            dictionary_name=dictionary_name,
            term=term,
            entity=term_update.entity,
            mapping_info=term_update.mapping
        )
        return {"message": f"Updated term '{term}' in dictionary '{dictionary_name}'"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update term: {str(e)}"
        )

@router.post("/upload")
async def upload_dictionary_file(
    file: UploadFile = File(...),
    dictionary_name: str = Form(...),
    is_new: bool = Form(False),
    version: Optional[str] = Form(None),
    current_user: User = Depends(check_admin_permission)
):
    """
    Upload a dictionary file
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JSON files are supported"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check dictionary quality
        warn_list, error_list = term_mapping_quality_check(file_content)
        
        if error_list:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": f"Dictionary contains {len(error_list)} errors",
                    "errors": error_list
                }
            )
        
        # Prepare dictionary name with version if needed
        upload_name = dictionary_name
        if not is_new and version:
            upload_name = f"{dictionary_name}_{version}"
        
        # Upload dictionary
        success, message, run_id = await upload_dictionary(
            file_content=file_content,
            dictionary_name=upload_name,
            file_name=file.filename
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message
            )
        
        return {
            "message": message,
            "run_id": run_id,
            "warnings": len(warn_list),
            "warning_list": warn_list if warn_list else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload dictionary: {str(e)}"
        )

@router.get("/job-status/{run_id}")
async def check_job_status(
    run_id: str,
    current_user: User = Depends(check_admin_permission)
):
    """
    Check the status of a dictionary processing job
    """
    try:
        status = await check_dictionary_job_status(run_id)
        return {"run_id": run_id, "status": status}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check job status: {str(e)}"
        )

@router.post("/quality-check")
async def check_dictionary_quality(
    file: UploadFile = File(...),
    current_user: User = Depends(check_admin_permission)
):
    """
    Check the quality of a dictionary file
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JSON files are supported"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check dictionary quality
        warn_list, error_list = term_mapping_quality_check(file_content)
        
        return {
            "warnings": len(warn_list),
            "errors": len(error_list),
            "warning_list": warn_list,
            "error_list": error_list
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check dictionary quality: {str(e)}"
        )

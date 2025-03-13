import json
from typing import List, Dict, Tuple, Any, Optional
from io import BytesIO

from app.services.aws_service import aws_service

async def list_dictionaries() -> List[str]:
    """
    List all available dictionaries
    """
    return await aws_service.list_dictionary_ids()

async def get_dictionaries_with_versions() -> Dict[str, List[str]]:
    """
    Get dictionaries with their versions
    """
    dictionaries = await list_dictionaries()
    return await aws_service.get_dict_with_version(dictionaries)

async def get_current_version(dict_id: str) -> Optional[str]:
    """
    Get the current version of a dictionary
    """
    return await aws_service.get_current_version(dict_id)

async def update_current_version(dict_id: str, version: str) -> None:
    """
    Update the current version of a dictionary
    """
    await aws_service.update_current_version(dict_id, version)

async def query_term(dictionary_name: str, term: str) -> Optional[Dict[str, Any]]:
    """
    Query a term from a dictionary
    """
    return await aws_service.query_term(dictionary_name, term)

async def update_term_mapping(dictionary_name: str, term: str, entity: str, mapping_info: Dict[str, List[str]]) -> None:
    """
    Update a term mapping in a dictionary
    """
    await aws_service.update_term_mapping(dictionary_name, term, entity, mapping_info)

async def upload_dictionary(file_content: bytes, dictionary_name: str, file_name: str) -> Tuple[bool, str, Optional[str]]:
    """
    Upload a dictionary file to S3 and start a Glue job to process it
    """
    # Upload to S3
    s3_key = f"translate/{dictionary_name}/{file_name}"
    success, message = await aws_service.upload_to_s3(file_content, s3_key)
    
    if not success:
        return False, message, None
    
    # Start Glue job
    run_id = await aws_service.start_glue_job(s3_key, dictionary_name)
    return True, "Dictionary uploaded and processing started", run_id

async def check_dictionary_job_status(run_id: str) -> str:
    """
    Check the status of a dictionary processing job
    """
    return await aws_service.get_glue_job_run_status(run_id)

def term_mapping_quality_check(file_content: bytes, min_length: int = 2) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Check the quality of a term mapping file
    """
    json_str = file_content.decode("utf-8")
    terminology_data = json.loads(json_str)

    error_list = []
    warn_list = []

    for entry in terminology_data['data']:
        mapping = entry['mapping']

        for language, terms in mapping.items():
            # Check if term is empty
            empty_term = False
            short_term = False
            for term in terms:
                # Check term length
                if len(term) == 0:
                    error_list.append(mapping)
                    empty_term = True
                elif len(term) < min_length:
                    warn_list.append(mapping)
                    short_term = True

                if empty_term or short_term:
                    break

            if empty_term or short_term:
                break

    return warn_list, error_list

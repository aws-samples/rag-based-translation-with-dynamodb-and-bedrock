from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class TranslationRequest(BaseModel):
    contents: List[str]
    source_lang: str
    target_lang: str
    dictionary_id: str
    model_id: str
    lambda_alias: str = "prod"

class TranslationResponse(BaseModel):
    translated_text: Optional[str] = None
    term_mapping: Optional[str] = None

class FileTranslationRequest(BaseModel):
    source_lang: str
    target_lang: str
    dictionary_id: str
    model_id: str
    concurrency: int = 3

class FileTranslationStats(BaseModel):
    total_sheets: int
    total_rows: int
    total_cells: int
    non_target_cells: int
    processing_time: float

class FileTranslationResponse(BaseModel):
    file_data: bytes
    stats: FileTranslationStats

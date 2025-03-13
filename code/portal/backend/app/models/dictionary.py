from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DictionaryTerm(BaseModel):
    term: str
    entity: Optional[str] = None
    mapping: Dict[str, List[str]]

class DictionaryTermUpdate(BaseModel):
    entity: Optional[str] = None
    mapping: Dict[str, List[str]]

class DictionaryVersion(BaseModel):
    dict_id: str
    versions: List[str]
    current_version: Optional[str] = None

class DictionaryVersionUpdate(BaseModel):
    version: str

class DictionaryQualityCheck(BaseModel):
    warnings: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]

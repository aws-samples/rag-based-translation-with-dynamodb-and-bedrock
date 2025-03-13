import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load config from YAML
config_yaml_path = os.path.join(BASE_DIR, "app", "core", "config.yaml")
with open(config_yaml_path, "r") as f:
    config_data = yaml.safe_load(f)

# Load user configurations from environment variables
def get_users_from_env() -> Dict[str, Tuple[str, str, str, str]]:
    """
    Parse user configurations from environment variables.
    Format: USER_<name>="username,email,role,password"
    Returns a dictionary with username as key and (username, email, role, password) as value.
    """
    users = {}
    user_pattern = re.compile(r'^USER_')
    
    for key, value in os.environ.items():
        if user_pattern.match(key):
            try:
                parts = value.split(',')
                if len(parts) == 4:
                    username, email, role, password = parts
                    users[username] = (username, email, role, password)
            except Exception as e:
                print(f"Error parsing user config {key}: {e}")
    
    # Add default users if no users are defined
    if not users:
        users["demo_user"] = ("demo_user", "demo@example.com", "user", "demo_password123")
        users["admin_user"] = ("admin_user", "admin@example.com", "admin", "admin_password456")
        users["super_admin"] = ("super_admin", "superadmin@example.com", "super-admin", "superadmin_password789")
    
    return users

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LLM Translate API"
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # AWS settings
    AWS_REGION: str = os.getenv("AWS_REGION", config_data.get("deploy_region", ["us-west-2"])[0])
    UPLOAD_BUCKET: str = os.getenv("UPLOAD_BUCKET", config_data.get("upload_bucket", {}).get("name", ""))
    TABLE_PREFIX: str = "translate_mapping_"
    
    # Supported languages and models
    SUPPORTED_LANGUAGES: Dict[str, str] = config_data.get("supportedlang", {})
    SUPPORTED_MODELS: List[str] = config_data.get("supportedmodel", [])
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Support contact
    SUPPORT_CONTACT: List[str] = config_data.get("support", ["support@example.com"])
    
    # User configurations
    USERS: Dict[str, Tuple[str, str, str, str]] = get_users_from_env()

settings = Settings()

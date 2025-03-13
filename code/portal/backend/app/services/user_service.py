from typing import Optional, Dict, List
import json
from app.models.user import User, UserInDB
from app.core.security import get_password_hash, verify_password
from app.core.config import settings

# Initialize users from environment variables
def initialize_users() -> Dict[str, UserInDB]:
    """
    Initialize users from environment variables defined in settings.
    """
    users_dict = {}
    
    for username, user_info in settings.USERS.items():
        username, email, role, password = user_info
        users_dict[username] = UserInDB(
            username=username,
            email=email,
            role=role,
            hashed_password=get_password_hash(password)
        )
    
    return users_dict

# Initialize the users database
users_db: Dict[str, UserInDB] = initialize_users()

async def get_user_by_username(username: str) -> Optional[User]:
    """
    Get a user by username.
    """
    if username in users_db:
        user_dict = users_db[username].dict()
        del user_dict["hashed_password"]
        return User(**user_dict)
    return None

async def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate a user with username and password.
    """
    user_dict = users_db.get(username)
    if not user_dict:
        return None
    if not verify_password(password, user_dict.hashed_password):
        return None
    
    user = User(
        username=user_dict.username,
        email=user_dict.email,
        role=user_dict.role
    )
    return user

async def get_all_users() -> List[User]:
    """
    Get all users (without password information).
    """
    users = []
    for username, user_data in users_db.items():
        user_dict = user_data.dict()
        del user_dict["hashed_password"]
        users.append(User(**user_dict))
    return users

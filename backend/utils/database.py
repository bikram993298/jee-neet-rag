import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import Optional, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "jee_neet_rag")

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]


def init_db():
    """Initialize database with indexes"""
    users_collection = db["users"]
    # Create unique index on email
    users_collection.create_index("email", unique=True)
    print("Database initialized with indexes")


class UserDB:
    """Database operations for users"""
    
    @staticmethod
    async def create_user(
        email: str,
        full_name: str,
        password_hash: str,
        email_verified: bool = False
    ) -> Dict[str, Any]:
        """Create a new user"""
        try:
            user_doc = {
                "email": email,
                "full_name": full_name,
                "password_hash": password_hash,
                "email_verified": email_verified,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
            
            result = db.users.insert_one(user_doc)
            user_doc["_id"] = result.inserted_id
            return user_doc
        except DuplicateKeyError:
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return db.users.find_one({"email": email})
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            return db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
    
    @staticmethod
    async def update_user(user_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update user details"""
        try:
            kwargs["updated_at"] = datetime.utcnow()
            result = db.users.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": kwargs},
                return_document=True
            )
            return result
        except Exception:
            return None
    
    @staticmethod
    async def verify_email(email: str) -> Optional[Dict[str, Any]]:
        """Mark email as verified"""
        try:
            result = db.users.find_one_and_update(
                {"email": email},
                {"$set": {"email_verified": True, "updated_at": datetime.utcnow()}},
                return_document=True
            )
            return result
        except Exception:
            return None
    
    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Delete user"""
        try:
            result = db.users.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    @staticmethod
    async def user_exists(email: str) -> bool:
        """Check if user exists by email"""
        return db.users.count_documents({"email": email}) > 0


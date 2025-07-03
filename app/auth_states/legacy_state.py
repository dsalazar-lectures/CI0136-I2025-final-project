"""
Legacy State Implementation Module.

This module implements the State pattern using the original code without design patterns.
"""
from typing import Dict, Any, Tuple, Optional
from flask import session
from ..models.services.registration_service import validate_login_data
from .auth_state_base import AuthState

class LegacyState(AuthState):
    """
    State implementation that uses the original code without refactoring.
    """
    
    def login(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Use the original login validation.
        """
        print("DEBUG: LegacyState - Login usando código original")
        email = credentials.get('email')
        password = credentials.get('password')
        return validate_login_data(email, password, user_repo)
    
    def setup_session(self, user: Dict[str, Any], session_obj) -> None:
        """
        Use the original session setup logic.
        """
        print("DEBUG: LegacyState - Setup session usando código original")
        session_obj.clear()
        session_obj["user_id"] = user["id"]
        session_obj["name"] = user.get("name", user.get("email"))
        session_obj["role"] = user["role"]
        session_obj["status"] = user.get("status")
        session_obj["email"] = user.get("email")
        session_obj["notification_enabled"] = user.get("notification_enabled", False)
    
    def google_login(self, token: str, user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Use the original Google login logic.
        """
        print("DEBUG: LegacyState - Google login usando código original")
        from firebase_admin import auth as firebase_auth
        
        try:
            decoded_token = firebase_auth.verify_id_token(token)
            email = decoded_token.get("email")
            name = decoded_token.get("name", email)
            
            existing_user = user_repo.get_user_by_email(email)
            
            if not existing_user:
                new_user = user_repo.add_user(
                    name=name,
                    email=email,
                    password=None,
                    role="Student"
                )
                
                if not new_user:
                    existing_user = user_repo.get_user_by_email(email)
                    if not existing_user:
                        return None, "Error al crear/recuperar usuario"
                else:
                    existing_user = new_user
            
            return existing_user, None
        except Exception as e:
            return None, str(e)

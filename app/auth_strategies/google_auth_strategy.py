"""
Google Auth Strategy Module.

This module implements the Google OAuth authentication strategy.
"""
from typing import Tuple, Dict, Any, Optional
import traceback
from firebase_admin import auth as firebase_auth
from ..auth_strategies.auth_strategy import AuthStrategy

class GoogleAuthStrategy(AuthStrategy):
    """
    Strategy for authenticating users with Google OAuth.
    """
    
    def authenticate(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using a Google ID token.
        
        Args:
            credentials: Dictionary containing 'token' (Google ID token).
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        try:
            id_token = credentials.get('token')
            
            # Verify and decode the token
            decoded_token = firebase_auth.verify_id_token(id_token)
            email = decoded_token.get("email")
            name = decoded_token.get("name", email)
            
            # Check if user exists
            existing_user = user_repo.get_user_by_email(email)
            
            if not existing_user:
                # Create new user if not exists
                new_user = user_repo.add_user(
                    name=name,
                    email=email,
                    password=None,
                    role="Student"
                )
                
                if not new_user:
                    # Try to retrieve again in case of race condition
                    existing_user = user_repo.get_user_by_email(email)
                    if not existing_user:
                        return None, "Error al crear/recuperar usuario"
                else:
                    existing_user = new_user
                    
                # Mark that this user was created via Google auth
                existing_user["auth_provider"] = "google"
            
            return existing_user, None
            
        except Exception as e:
            traceback.print_exc()
            return None, str(e)
        
    def setup_session(self, user: Dict[str, Any], session) -> None:
        """
        Setup the session for a Google authenticated user.
        
        Args:
            user: User data dictionary.
            session: Flask session object.
        """
        # Clear any existing session data
        session.clear()
        
        # Set up the session with user data
        session["user_id"] = user["id"]
        session["email"] = user["email"]
        session["name"] = user.get("name", user["email"])
        session["role"] = user["role"]
        session["status"] = user["status"]
        session["auth_provider"] = "google"

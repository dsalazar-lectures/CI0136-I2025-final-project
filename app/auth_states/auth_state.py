"""
Auth State Pattern Module.

This module implements the State pattern for toggling between the original code
and the refactored version with design patterns.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
from flask import session
from ..auth_strategies.auth_strategy_factory import AuthStrategyFactory
from ..models.services.registration_service import validate_login_data
import os
import pathlib

def get_use_patterns():
    """
    Lee directamente la configuración del archivo .env.
    
    Esta función ignora el mecanismo de variables de entorno y lee
    directamente del archivo para evitar problemas de caché.
    
    Returns:
        bool: True si FLASK_USE_PATTERNS=True, False en caso contrario
    """
    try:
        # Obtener la ruta absoluta del proyecto
        project_root = pathlib.Path(__file__).parent.parent.parent
        env_path = project_root / '.env'
        
        # Leer el archivo .env
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('FLASK_USE_PATTERNS='):
                    value = line.strip().split('=')[1]
                    return value.lower() == 'true'
    except Exception as e:
        print(f"Error leyendo .env: {e}")
    
    return False  # valor por defecto

class AuthState(ABC):
    """
    Abstract State base class for authentication.
    
    This defines the interface for different authentication state implementations.
    """
    
    @abstractmethod
    def login(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using the provided credentials.
        
        Args:
            credentials: Dictionary containing authentication credentials.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        pass
    
    @abstractmethod
    def setup_session(self, user: Dict[str, Any], session_obj) -> None:
        """
        Set up the user session after successful authentication.
        
        Args:
            user: User data dictionary.
            session_obj: Flask session object.
        """
        pass
    
    @abstractmethod
    def google_login(self, token: str, user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Authenticate a user using Google authentication.
        
        Args:
            token: Google ID token.
            user_repo: Repository object for user data operations.
            
        Returns:
            A tuple containing (user_data, error_message).
        """
        pass

class PatternState(AuthState):
    """
    State implementation that uses the refactored code with design patterns.
    """
    
    def login(self, credentials: Dict[str, Any], user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Use the refactored authentication strategy pattern.
        """
        print("DEBUG: PatternState - Login usando Strategy Pattern")
        auth_strategy = AuthStrategyFactory.create_strategy("local")
        return auth_strategy.authenticate(credentials, user_repo)
    
    def setup_session(self, user: Dict[str, Any], session_obj) -> None:
        """
        Use the refactored session setup from auth strategy.
        """
        print("DEBUG: PatternState - Setup session usando Strategy Pattern")
        auth_strategy = AuthStrategyFactory.create_strategy("local")
        auth_strategy.setup_session(user, session_obj)
    
    def google_login(self, token: str, user_repo) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Use the refactored Google authentication strategy.
        """
        print("DEBUG: PatternState - Google login usando Strategy Pattern")
        auth_strategy = AuthStrategyFactory.create_strategy("google")
        credentials = {'token': token}
        return auth_strategy.authenticate(credentials, user_repo)

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

class AuthStateContext:
    """
    Context class that manages the current authentication state.
    """
    
    @staticmethod
    def get_state() -> AuthState:
        """
        Get the appropriate authentication state based on environment configuration.
        
        Returns:
            An instance of the appropriate AuthState implementation.
        """
        # Usamos la función get_use_patterns() para leer directamente del archivo .env
        use_patterns = get_use_patterns()
        
        # Print simple para validar el estado actual
        current_state = "PatternState (usando Strategy Pattern)" if use_patterns else "LegacyState (usando código original)"
        print("\n==================================================")
        print(f"ESTADO ACTUAL: {current_state}")
        print("==================================================\n")
        
        if use_patterns:
            return PatternState()
        else:
            return LegacyState()

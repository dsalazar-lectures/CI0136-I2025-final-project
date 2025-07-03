"""
Auth State Context Module.

This module defines the context class that manages the current authentication state.
"""
from .auth_state_base import AuthState
from .pattern_state import PatternState
from .legacy_state import LegacyState
from .utils import get_use_patterns

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

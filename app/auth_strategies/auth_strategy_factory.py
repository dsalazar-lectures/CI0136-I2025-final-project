"""
Auth Strategy Factory Module.

This module provides a factory for creating authentication strategy instances.
"""
from typing import Dict, Any, Optional
from ..auth_strategies.auth_strategy import AuthStrategy
from ..auth_strategies.local_auth_strategy import LocalAuthStrategy
from ..auth_strategies.google_auth_strategy import GoogleAuthStrategy

class AuthStrategyFactory:
    """
    Factory for creating authentication strategy instances.
    """
    
    @staticmethod
    def create_strategy(provider: str) -> Optional[AuthStrategy]:
        """
        Create an authentication strategy based on the provider type.
        
        Args:
            provider: The authentication provider type ("local" or "google").
            
        Returns:
            An instance of the appropriate AuthStrategy implementation,
            or None if the provider is not supported.
        """
        if provider == "local":
            return LocalAuthStrategy()
        elif provider == "google":
            return GoogleAuthStrategy()
        else:
            return None

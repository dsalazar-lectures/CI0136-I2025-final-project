"""
Registration Strategy Factory Module.

This module provides a factory for creating registration strategy instances.
"""
from typing import Optional
from ..auth_strategies.registration_strategy import RegistrationStrategy
from ..auth_strategies.local_registration_strategy import LocalRegistrationStrategy
from ..auth_strategies.google_registration_strategy import GoogleRegistrationStrategy

class RegistrationStrategyFactory:
    """
    Factory for creating registration strategy instances.
    """
    
    @staticmethod
    def create_strategy(provider: str) -> Optional[RegistrationStrategy]:
        """
        Create a registration strategy based on the provider type.
        
        Args:
            provider: The registration provider type ("local" or "google").
            
        Returns:
            An instance of the appropriate RegistrationStrategy implementation,
            or None if the provider is not supported.
        """
        if provider == "local":
            return LocalRegistrationStrategy()
        elif provider == "google":
            return GoogleRegistrationStrategy()
        else:
            return None

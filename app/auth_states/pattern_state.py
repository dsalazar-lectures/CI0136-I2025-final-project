"""
Pattern State Implementation Module.

This module implements the State pattern using design patterns (Strategy, Factory).
"""
from typing import Dict, Any, Tuple, Optional
from flask import session
from ..auth_strategies.auth_strategy_factory import AuthStrategyFactory
from .auth_state_base import AuthState

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

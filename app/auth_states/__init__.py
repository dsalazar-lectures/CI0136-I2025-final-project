"""
Auth States Package.

This package implements the State pattern for toggling between
original code and refactored code with design patterns.
"""
from .auth_state_base import AuthState
from .pattern_state import PatternState
from .legacy_state import LegacyState
from .auth_state_context import AuthStateContext
from .utils import get_use_patterns

# Expose only what's needed to the outside
__all__ = ['AuthState', 'PatternState', 'LegacyState', 'AuthStateContext', 'get_use_patterns']

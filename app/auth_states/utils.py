"""
Utility functions for Auth State Pattern.

This module provides utility functions for the Auth State Pattern implementation.
"""
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

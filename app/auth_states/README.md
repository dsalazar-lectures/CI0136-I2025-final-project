# Auth State Pattern

Este directorio implementa el patrón State para permitir alternar entre la versión original del código y la versión refactorizada con patrones de diseño.

## Arquitectura

- `auth_state.py`: Define la interfaz `AuthState` y dos implementaciones concretas:
  - `PatternState`: Utiliza el código refactorizado con patrones de diseño (Strategy, Factory, etc.)
  - `LegacyState`: Utiliza el código original sin refactorizar

## Control de Estados

El sistema determina qué implementación usar basándose en la variable de entorno `FLASK_USE_PATTERNS` definida en el archivo `.env` en la raíz del proyecto:

- `FLASK_USE_PATTERNS=True`: Usa la versión refactorizada con patrones de diseño
- `FLASK_USE_PATTERNS=False`: Usa la versión original sin refactorizar

## Uso

Para cambiar entre las implementaciones, simplemente modifique el valor de la variable `FLASK_USE_PATTERNS` en el archivo `.env` y reinicie la aplicación.

## Ventajas

1. **Transición gradual**: Permite una transición controlada entre el código antiguo y el nuevo
2. **Testing A/B**: Facilita comparar el comportamiento entre ambas implementaciones
3. **Rollback rápido**: En caso de problemas, permite volver rápidamente a la implementación anterior
4. **Separación de responsabilidades**: Mantiene el código de ambas implementaciones bien organizado

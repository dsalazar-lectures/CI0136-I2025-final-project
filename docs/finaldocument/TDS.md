# Buenas Prácticas de Ingeniería de Software - Sistema de Reviews y Comentarios

## Tronaditas


## Buenas Prácticas de Ingeniería de Software Implementadas

### 1. **Separación de Responsabilidades**
- **Controladores**: Manejan la lógica HTTP y redirecciones (`review_controller.py`)
- **Modelos**: Gestionan la persistencia y lógica de datos (`review_model.py`)
- **Rutas**: Definen endpoints y delegan a controladores (`review_routes.py`)
- **Presentadores**: Manejan la notificación y presentación (`review_presenter_controller.py`)

### 2. **Validación y Seguridad Robusta**
- Validación de entrada en múltiples capas
- Filtrado de inyección SQL y XSS
- Detección de lenguaje ofensivo
- Validación de autorización y roles

### 3. **Manejo de Errores Consistente**
- Mensajes de error claros y específicos
- Redirecciones apropiadas en caso de error
- Logging de errores para debugging

### 4. **Persistencia de Datos**
- Almacenamiento local en JSON para desarrollo
- Sincronización con Firestore para producción
- Respaldo automático en ambos sistemas

---

## Patrones de Diseño Implementados

### **Patrón 1: Strategy Pattern**

**Funcionalidad que usa el patrón:**
Sistema de presentación de reviews con diferentes estrategias de notificación (consola, email, logs).

**Nombre del patrón:**
**Strategy Pattern (Patrón Estrategia)**

**Descripción clara del patrón:**
Define una familia de algoritmos, los encapsula y los hace intercambiables. Permite que el algoritmo varíe independientemente de los clientes que lo usan.

**Motivación de uso:**
- Evitar condicionales extensas para diferentes tipos de notificación
- Permitir agregar nuevos tipos de presentación sin modificar código existente
- Desacoplar la lógica de notificación del controlador principal

**Implementación y guía de extensión:**

```python
# Interfaz base abstracta
class ReviewPresenterStrategy(ABC):
    @abstractmethod
    def present_review(self, review):
        pass

# Estrategias concretas
class ConsoleReviewPresenter(ReviewPresenterStrategy):
    def present_review(self, review):
        print(f"Nueva reseña: {review['comment']}")

class EmailReviewPresenter(ReviewPresenterStrategy):
    def present_review(self, review):
        # Envía notificación por email
        
class LogFileReviewPresenter(ReviewPresenterStrategy):
    def present_review(self, review):
        # Registra en archivo de log
```

**Para extender:**
1. Crear nueva clase que herede de `ReviewPresenterStrategy`
2. Implementar el método `present_review()`
3. Instanciar y usar en el controlador sin modificar código existente
4. Ejemplo: `SMSReviewPresenter`, `SlackReviewPresenter`

---

### **Patrón 2: Singleton Pattern**

**Funcionalidad que usa el patrón:**
Gestión centralizada de reviews a través de `ReviewManager`.

**Nombre del patrón:**
**Singleton Pattern (Patrón Singleton)**

**Descripción clara del patrón:**
Garantiza que una clase tenga solo una instancia y proporciona un punto de acceso global a ella.

**Motivación de uso:**
- Evitar múltiples instancias de gestores de datos
- Centralizar el acceso a la base de datos
- Mantener consistencia en las operaciones CRUD

**Implementación y guía de extensión:**

```python
class ReviewManager:
    def __init__(self):
        # Inicialización de Firebase y rutas
        
# Instancia singleton
review_manager = ReviewManager()

# Funciones facade que delegan al singleton
def get_all_reviews():
    return review_manager.get_all_reviews()

def add_review(review):
    return review_manager.add_review(review)
```

**Para extender:**
1. Utilizar las funciones facade existentes (`get_all_reviews`, `add_review`, etc.)
2. Agregar nuevos métodos al `ReviewManager` según necesidades
3. Crear nuevas funciones facade para mantener la interfaz simple
4. Evitar instanciar `ReviewManager` directamente

---

### **Patrón 3: Template Method Pattern (Implícito)**

**Funcionalidad que usa el patrón:**
Flujo común de validación y procesamiento de reviews.

**Nombre del patrón:**
**Template Method Pattern (Método Plantilla)**

**Descripción clara del patrón:**
Define el esqueleto de un algoritmo en una operación, delegando algunos pasos a subclases. Las subclases pueden redefinir pasos específicos sin cambiar la estructura general.

**Motivación de uso:**
- Estandarizar el flujo de validación de reviews
- Permitir reutilización del código de validación
- Mantener consistencia en el procesamiento

**Implementación y guía de extensión:**

```python
def send_review(tutoria=None):
    # 1. Validar rol del usuario
    if session.get('role') != 'Student':
        # Manejo de error
    
    # 2. Validar inscripción en tutoría
    if not exists:
        # Manejo de error
    
    # 3. Validar datos de entrada
    if not rating or not comment.strip():
        # Manejo de error
    
    # 4. Filtros de seguridad
    if is_injection(comment) or is_offensive(comment):
        # Manejo de error
    
    # 5. Procesar y guardar
    review = crear_review(datos)
    add_review(review)
    
    # 6. Notificar
    presentar_review(review)
```

**Para extender:**
1. Seguir la misma secuencia para nuevos tipos de contenido
2. Extraer validaciones comunes a funciones reutilizables
3. Personalizar pasos específicos según el tipo de operación
4. Mantener el orden: validación → procesamiento → persistencia → notificación

---

### **Patrón 4: Facade Pattern**

**Funcionalidad que usa el patrón:**
Interfaz simplificada para operaciones complejas de gestión de reviews que involucran múltiples subsistemas (JSON, Firestore, validaciones).

**Nombre del patrón:**
**Facade Pattern (Patrón Fachada)**

**Descripción clara del patrón:**
Proporciona una interfaz simplificada a un conjunto de interfaces en un subsistema. Define una interfaz de nivel superior que hace que el subsistema sea más fácil de usar.

**Motivación de uso:**
- Simplificar el acceso a operaciones complejas de persistencia
- Ocultar la complejidad de la sincronización entre JSON y Firestore
- Proporcionar una API limpia y consistente para los controladores
- Centralizar la lógica de acceso a datos

**Implementación y guía de extensión:**

```python
# ReviewManager actúa como el subsistema complejo
class ReviewManager:
    def __init__(self):
        # Inicialización de Firebase y configuración
        self.db = firestore.client()
        self.json_path = Path(__file__).parent / "reviews_data.json"
    
    def get_all_reviews(self):
        # Lógica compleja: intenta Firestore, fallback a JSON
        pass
    
    def add_review(self, review):
        # Lógica compleja: guarda en JSON Y Firestore
        pass

# Instancia del subsistema
review_manager = ReviewManager()

# FACADE: Funciones simples que ocultan la complejidad
def get_all_reviews():
    """Facade simple para obtener todas las reviews"""
    return review_manager.get_all_reviews()

def add_review(review):
    """Facade simple para agregar una review"""
    return review_manager.add_review(review)

def get_review_by_id(review_id):
    """Facade simple para obtener review por ID"""
    return review_manager.get_review_by_id(review_id)

def update_review(review_id, rating, comment, drive_link=""):
    """Facade simple para actualizar review"""
    return review_manager.update_review(review_id, rating, comment, drive_link)

def delete_review(review_id):
    """Facade simple para eliminar review"""
    return review_manager.delete_review(review_id)
```

**Para extender:**
1. **Para nuevas operaciones**: Agregar método al `ReviewManager` y crear función facade correspondiente
2. **Para nuevos tipos de persistencia**: Modificar internamente `ReviewManager` sin cambiar las funciones facade
3. **Para mantener compatibilidad**: Los controladores solo usan las funciones facade, nunca `ReviewManager` directamente
4. **Ejemplo de extensión**:
   ```python
   # En ReviewManager
   def get_reviews_by_rating(self, min_rating):
       # Lógica compleja
   
   # Facade correspondiente
   def get_reviews_by_rating(min_rating):
       return review_manager.get_reviews_by_rating(min_rating)
   ```

**Beneficios obtenidos:**
- Los controladores usan `add_review(review)` en lugar de manejar JSON + Firestore
- Cambios en la persistencia no afectan a los controladores
- Interfaz consistente y predecible
- Facilita testing al poder mockear las funciones facade

---

## Funcionalidades de Seguridad Implementadas

### **Filtrado de Inyección de Código**
```python
def is_injection(comment):
    suspicious_patterns = [
        r"('|--|;)",                     # SQL básico
        r"(drop\s+table|insert\s+into)", # SQL avanzado
        r"<script.*?>.*?</script>",      # XSS
        r"(alert\s*\(|confirm\s*\()",    # JavaScript
        r"`.*?`",                        # Command injection
        r"\$\{.*?\}",                   # Template injection
    ]
```

### **Detección de Lenguaje Ofensivo**
- Uso de la librería `better-profanity`
- Filtrado automático de contenido inapropiado
- Bloqueo preventivo con mensajes claros

### **Control de Autorización**
- Validación de roles (solo estudiantes pueden comentar)
- Verificación de inscripción en tutorías
- Control de acceso a funciones de edición/eliminación

---

## Aspectos que No Salieron Tan Bien

### **1. Acoplamiento entre Componentes**
**Problema:** El controlador de reviews tiene dependencias directas con múltiples servicios.
```python
from app.models.review_model import add_review, get_all_reviews, ...
from app.controllers.review_presenter_controller import ConsoleReviewPresenter, EmailReviewPresenter
```

**Mejora sugerida:** Implementar inyección de dependencias.

### **2. Validaciones Dispersas**
**Problema:** La lógica de validación está mezclada en el controlador principal.

**Mejora sugerida:** 
- Crear un servicio dedicado de validación
- Implementar el patrón Chain of Responsibility para validaciones
- Separar validaciones de negocio de validaciones técnicas

### **3. Manejo de Estado Inconsistente**
**Problema:** Sincronización manual entre JSON local y Firestore.

**Mejora sugerida:**
- Implementar patrón Repository para abstraer persistencia
- Usar eventos para sincronización automática

### **4. Testing Limitado**
**Problema:** Tests fragmentados y mock excesivo sin tests de integración.

**Evidencia:** Los tests requieren muchos mocks para funcionar:
```python
@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_comments_appear_in_tutor_profile(mock_user_repo, mock_get_reviews, client):
```

**Mejora sugerida:**
- Implementar tests de integración con base de datos de prueba
- Reducir dependencia de mocks
- Crear fixtures reutilizables

---

## Trabajo Pendiente y Razones

### **1. Sistema de Moderación Avanzado**
**Pendiente:** Implementar un sistema de moderación con revisión humana.
**Razón:** Las validaciones automáticas no capturan todos los casos problemáticos.

### **2. Notificaciones en Tiempo Real**
**Pendiente:** WebSockets para notificaciones instantáneas.
**Razón:** Complejidad adicional.

### **4. Analytics de Reviews**
**Pendiente:** Dashboard para análisis de sentimientos y métricas.
**Razón:** Requiere integración con servicios externos.

### **5. Versionado de Reviews**
**Pendiente:** Historial de cambios en comentarios editados.
**Razón:** Complejidad de implementación vs. beneficio percibido.

---

## Conclusiones

El sistema de reviews y comentarios implementa patrones de diseño sólidos y buenas prácticas de seguridad. Sin embargo, presenta oportunidades de mejora en arquitectura, testing y separación de responsabilidades. Las funcionalidades pendientes reflejan decisiones pragmáticas de priorización en un contexto académico con limitaciones de tiempo.

### **Fortalezas Principales:**
- Validación robusta de entrada
- Patrones de diseño bien aplicados
- Manejo de errores consistente
- Notificaciones múltiples implementadas

### **Áreas de Mejora Prioritarias:**
- Inyección de dependencias
- Tests de integración
- Refactoring de validaciones
- Abstracciones de persistencia


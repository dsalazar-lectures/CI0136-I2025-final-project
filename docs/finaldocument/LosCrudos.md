# Final Report – Software Engineering Practices and Design Patterns

## Good Software Engineering Practices

Throughout the development of the project, we applied several software engineering best practices to keep our code clean, organized, and maintainable:

- **Separation of concerns**: we structured the code into distinct layers for business logic, presentation logic, and data access.
- **Version control**: we used Git and GitHub for version management and effective team collaboration.
- **Modularity**: reusable modules were created for components, services, and repositories.
- **Clear naming conventions**: meaningful names were used for functions, classes, and variables.
- **Basic documentation**: each complex module contains explanatory comments for better understanding.
- **Frequent manual testing**: we continuously validated key features to ensure functionality remained intact after changes.

## SOLID Principles Applied

During development, we also aimed to follow the SOLID principles, which are essential for writing scalable and maintainable object-oriented code:

### 1. **Single Responsibility Principle (SRP)**  
- **Applied in**: repositories, services, and strategy classes.  
- **Explanation**: each class or module has one clearly defined responsibility. For example, repositories are only responsible for database access, and services handle business logic.  
- **Benefits**: this separation makes the code easier to test and modify independently.

---

### 2. **Open/Closed Principle (OCP)**  
- **Applied in**: Strategy and Factory patterns.  
- **Explanation**: our code is open for extension but closed for modification. We can add new strategies for filtering or new button types without changing existing logic.  

---

### 3. **Liskov Substitution Principle (LSP)**  
- **Applied in**: all Strategy and Factory implementations.  
- **Explanation**: all child classes (strategies or buttons) can replace their base class/interface without breaking functionality.  
- **Example**: a `ZoomButton` can be used wherever a base button is expected.

---

### 4. **Interface Segregation Principle (ISP)**  
- **Applied in**: Strategy pattern interfaces.  
- **Explanation**: clients only depend on the methods they actually use. Each filtering strategy implements only the filtering logic, without being forced to implement unrelated methods.  
- **Result**: cleaner and more focused strategy classes.

---

### 5. **Dependency Inversion Principle (DIP)**  
- **Applied in**: service layers using repositories and strategies.  
- **Explanation**: high-level modules (services) do not depend on low-level modules (DB logic or filtering implementation). Instead, they depend on abstractions. 

---

## Design Patterns Used

### 1. Repository Pattern

- **Functionality**: database interaction.
- **Pattern name**: Repository.
- **Description**: the Repository pattern acts as a mediator between the domain and data mapping layers. It abstracts data access logic and centralizes it in a repository class, hiding the underlying database details.
- **Motivation**: we needed to decouple our business logic from database operations, allowing for easier testing and future changes in the persistence layer.
- **Implementation & Extension Guide**:
  - Files are located in `models/repositories/tutorial`.
  - Each entity has its own repository file (e.g., `tutorial.py`).
  - To extend:
    - Create a `NewEntityRepository.py`.
    - Implement standard methods like `findAll`, `findById`, `create`, `update`, and `delete`.
    - Export the class and use it within service files.
    - Follow the naming and structure conventions established by existing repositories.

---

### 2. Factory Pattern

- **Functionality**: dynamic button creation (e.g., zoom button).
- **Pattern name**: Factory Method.
- **Description**: the Factory pattern encapsulates the object creation logic and provides a common interface for creating instances of related classes without specifying the concrete class.
- **Motivation**: we needed to generate various button types with different styles and behaviors (zoom, etc.) without duplicating code or relying on conditional logic.
- **Implementation & Extension Guide**:
  - Located in `models/builders/button_factory`.
  - We use `button_factory.create_button(type)` to return the correct button instance.
  - Each type has its own button class (e.g., `ZoomButton`).
  - To add a new type:
    - Create a new button class.
    - Register it inside the `button_factory`.
    - Use `button_factory.create_button('newType')` wherever needed in the frontend.

---

### 3. Strategy Pattern

- **Functionality**: filtering strategies for tutoring sessions.
- **Pattern name**: Strategy.
- **Description**: the Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It allows for varying behavior without modifying the class that uses it.
- **Motivation**: we needed to apply different filter criteria (by date, by subject, by tutor) in a flexible and maintainable way.
- **Implementation & Extension Guide**:
  - Strategy classes are located in `models/storting_strategies/strategies`, with supporting logic in `services/tutorials`.
  - Each strategy (e.g., `ascending_date.py`, `descending_date.py`) implements a common filtering interface.
  - `tutorial_utils.py` selects and applies the strategy based on the current filtering needs.
  - To extend:
    - Create a new strategy class implementing a `filter(data, criteria)` method.
    - Add it to the strategy registry or context.
    - Make sure the UI or service layer can reference it dynamically.

---

## Challenges and Areas for Improvement

- **Limited error handling**: some routes and services lack robust exception handling. A more centralized and consistent error management system would be beneficial.
- **Communication gaps**: occasional miscommunications led to duplicated or misunderstood tasks. Holding more frequent check-in meetings could prevent this in future projects.
- **Inter-group coordination**: collaboration with other teams working on related components was limited. Establishing clearer integration guidelines and shared APIs would improve consistency and reduce friction in future iterations.
- **Pending work**:
  - Deeper backend validation rules.
  - A more complete admin module with user role control.
  - UI improvements for mobile responsiveness and cross-browser testing.

---


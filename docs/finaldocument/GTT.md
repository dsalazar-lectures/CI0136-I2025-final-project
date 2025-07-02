# **Software Engineering Best Practices Followed by the Code**

During the development of the system, several best practices were applied that promote quality, scalability, and maintainability. The most relevant include:

* **Application of SOLID Principles:**

  * **S – Single Responsibility Principle:** Each class has a specific role. For example, the `AuthStrategy`, `GoogleAuthStrategy`, etc., handle authentication only, separated from the controller.
  * **O – Open/Closed Principle:** New authentication or registration strategies can be added without modifying existing ones, thanks to the use of interfaces and factories.
  * **L – Liskov Substitution Principle:** Subclasses like `LocalAuthStrategy` and `GoogleAuthStrategy` can be used without altering the behavior of the system.
  * **I – Interface Segregation Principle:** Interfaces like `AuthStrategy` and `RegistrationStrategy` are designed with specific methods, avoiding forcing classes to implement unused functionalities.
  * **D – Dependency Inversion Principle:** The system relies on abstractions rather than concrete implementations, using factories to instantiate the strategies.

* **Decoupling and Modularity:**
  The system is divided into well-defined modules (strategies, services, controllers, states), allowing functionality to be maintained and extended with minimal impact.

* **Use of Recognized Design Patterns:**
  Strategy, Factory Method, Decorator, Template Method, and State patterns were properly applied, improving code structure and adaptability.

* **Logic Reuse through Decorators:**
  Access control to routes was centralized in the `login_or_role_required` decorator, removing redundant validations from the controllers.

* **Clear Separation Between Presentation and Business Logic:**
  Controllers manage views and HTTP interaction, while the authentication and registration logic is fully isolated in the corresponding strategies.

* **Validation and Error Handling from Early Stages:**
  Immediate validation was implemented in forms, and errors are handled with clear messages and appropriate redirection, enhancing the user experience.

---

## **Applied Design Patterns**

### **Pattern 1: Strategy**

* **Functionality that uses the pattern:**
  User authentication (`AuthStrategy`) and registration (`RegistrationStrategy`) with different providers (local, Google, etc.).

* **Pattern Name:**
  **Strategy Pattern**

* **Description:**
  This pattern defines a family of algorithms, encapsulates each one, and allows them to be interchangeable without affecting the clients that use them.

* **Motivation:**
  To avoid extensive conditional structures within controllers (`login`, `register`) and allow new strategies to be integrated without altering the main flow.

* **Implementation and Extension Guide:**
  Interfaces `AuthStrategy` and `RegistrationStrategy` were defined, implemented by classes like `LocalAuthStrategy`, `GoogleAuthStrategy`, etc. To extend the system, a new class can inherit from these interfaces, implement the required methods, and be registered in the corresponding factories.

---

### **Pattern 2: Factory Method**

* **Functionality that uses the pattern:**
  Creating instances of authentication or registration strategies based on an identifier (`"local"`, `"google"`).

* **Pattern Name:**
  **Factory Method**

* **Description:**
  This pattern delegates object creation to subclasses, removing the need for client code to know the concrete classes being used.

* **Motivation:**
  To centralize the construction logic of strategies and maintain decoupling from the controller.

* **Implementation and Extension Guide:**
  `AuthStrategyFactory` and `RegistrationStrategyFactory` classes implement `create_strategy(provider: str)` methods that return the corresponding strategy. To extend, simply add a new entry to the method’s conditional and return the new implemented strategy.

---

### **Pattern 3: Template Method (Implicit)**

* **Functionality that uses the pattern:**
  Common flow in `register` and `google_register` methods: gather data → create strategy → authenticate/register → process result.

* **Pattern Name:**
  **Template Method**

* **Description:**
  This pattern defines the skeleton of an algorithm, delegating some steps to subclasses. Subclasses can redefine parts without changing the overall structure.

* **Motivation:**
  Since the user registration flow is common, this pattern was implicitly used to reuse that structure while allowing behavior customization based on the provider.

* **Implementation and Extension Guide:**
  Registration strategies implement `authenticate` and `process_registration_result`, which are invoked by the controller following a shared structure. To extend, follow this sequence or formally define base methods in `RegistrationStrategy` as hooks.

---

### **Pattern 4: Decorator**

* **Functionality that uses the pattern:**
  Route access control in Flask, ensuring users are authenticated and, optionally, have a specific role.

* **Pattern Name:**
  **Decorator Pattern**

* **Description:**
  Adds additional functionality to existing functions without modifying their structure. Here, it encapsulates session and role validation logic in a decorator.

* **Motivation:**
  To keep security logic decoupled from controllers and avoid repeating it across routes.

* **Implementation and Extension Guide:**
  The `login_or_role_required(required_role=None)` decorator redirects unauthenticated users to the login and returns 403 errors for unauthorized roles. It uses `@wraps` to preserve metadata. To extend, you can support multiple roles, create aliases like `@admin_required`, or use constants to prevent typos.

---

### **Pattern 5: State**

* **Functionality that uses the pattern:**
  Dynamic switching between two authentication handling methods: one based on legacy code and another using design patterns. The selection is made based on a `.env` configuration.

* **Pattern Name:**
  **State Pattern**

* **Description:**
  The State pattern allows an object to change its behavior at runtime depending on its internal state. Each state is encapsulated in a class implementing a shared interface.

* **Motivation:**
  A flexible way was needed to switch between legacy and refactored code without duplicating logic in controllers or complicating maintenance. This supports progressive evolution of the system.

* **Implementation and Extension Guide:**

  * An abstract interface `AuthState` was defined with methods `login`, `setup_session`, and `google_login`.
  * Classes `LegacyState` and `PatternState` implement this interface, representing the two authentication variants.
  * The `AuthStateContext` selects the appropriate implementation at runtime using the `get_use_patterns()` function that reads from the `.env` file.

  To extend:

  1. Create a new class inheriting from `AuthState` to represent a new authentication method.
  2. Implement the required logic in its methods.
  3. Update `AuthStateContext` to include the new option based on the desired configuration.

---

## **Aspects That Could Be Improved**

Several areas for improvement were identified during the development of the system, both technical and organizational:

* **Lack of coordination in team collaboration:**
  Team collaboration was inconsistent and not fluid, which impacted code consistency and made it harder to maintain a clear, coherent structure across modules.

* **Code with mixed responsibilities:**
  In some parts of the system, business and control logic are coupled, violating the separation of concerns principle. Better initial project organization could have prevented this.

* **Time pressure from other courses:**
  The academic load from other courses significantly affected planning and pace. Many tasks were postponed to later stages, reducing time available for reviewing, refactoring, and standardizing the code.

* **Inconsistent visual design (look and feel):**
  The interface lacks a unified graphic style. The absence of a style guide or reusable components from the start caused visual inconsistencies across views.

* **Limited Continuous Integration:**
  No CI process was established to automatically verify changes merged into the `main` branch. As a result, some issues were detected late during manual integrations, complicating a smooth and safe integration process.

---

## **Testing Approach and Achievements**

The project implemented a comprehensive testing strategy to ensure functionality, quality, and robustness of the code base. This approach helped identify issues early in the development process and provided confidence in the implemented features.

### **Testing Framework and Structure**

* **Framework Used:**
  The testing was implemented using pytest, a powerful Python testing framework that facilitates both simple unit tests and complex functional tests.

* **Test Organization:**
  Tests were organized by functionality, with dedicated test files for each major component of the system (authentication, profile editing, password management, etc.).

* **Mocking and Fixtures:**
  Extensive use of fixtures and mocking facilitated isolated testing without external dependencies. For example, database connections were mocked to prevent test execution from affecting production data.

### **Test Coverage Areas**

1. **Authentication Testing:**
   * Validation of login credentials
   * Testing of authentication strategies (local and Google)
   * Role-based access control verification
   * Session management testing

2. **User Management Testing:**
   * Registration validation and error handling
   * Profile editing functionality
   * Password strength validation and security
   * Role assignment and permissions

3. **Functionality Testing:**
   * Tutoring session creation and management
   * Reviews and ratings system
   * Comment functionality
   * Subscription management

4. **Integration Testing:**
   * End-to-end flows for critical user journeys
   * State transitions throughout the application

### **Key Testing Achievements**

* **Robust Error Handling:**
  Tests verified that the system properly validates inputs and provides clear error messages when invalid data is provided.

* **Session Management:**
  Special attention was given to testing session persistence and security, ensuring user state is properly maintained between requests.

* **Cross-Component Integration:**
  Tests verified that components interact correctly, particularly between the authentication system, user profiles, and feature access.

* **Design Pattern Verification:**
  The implemented tests validated that design patterns (Strategy, Factory, State) function as intended and maintain expected behavior.
  
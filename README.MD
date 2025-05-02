# Tutoring Project - Flask (Monolithic MVC Architecture)

## General Description

This project consists of developing a web platform for tutoring management using Flask with a monolithic architecture based on the MVC (Model-View-Controller) pattern. It will allow the creation, modification, and deletion of tutoring sessions, as well as user management with different roles (student, tutor, administrator).

---

## Architecture

The project follows a **monolithic MVC architecture** with the following folder structure:

```
/TutoringProject
│
├── /app                  # Main application directory
│   ├── /controllers       # Controllers - Business logic and route handling
│   ├── /models            # Models - Database and related logic
│   ├── /views             # Views - HTML templates and static files
│   ├── /routes            # Routes defined via Blueprints
│   ├── /static            # CSS, JS, and images
│   ├── /templates         # HTML templates (Jinja2)
│   ├── __init__.py        # Flask application initialization
│   └── app.py             # Main file to run the application
├── /migrations            # Database migrations
├── /tests                 # Unit and integration tests
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

### **Coding Conventions (PEP 8)**

- All functions, variables, and files use `snake_case`.
- Classes use `PascalCase`.
- Files and folders follow the `snake_case` standard.
- URLs use `kebab-case`.
- Constant names use `UPPER_SNAKE_CASE`.
- Follow PEP 8 recommendations for indentation (4 spaces), line length, comments, and documentation.

---

## Version Control (Git Workflow)

The workflow follows a branching scheme organized by features and sprints.

- **Branches:**

  - `main`: Main production branch.
  - `dev`: Common development branch per sprint.
  - `feature/<feature_name>`: Specific branches for each new feature.

- **Pull Requests:**

  - From `feature` to `dev`: Reviewed by at least one person from the team.
  - From `dev` to `main`: Reviewed by at least one person from the group.
  - Each PR must include:
    - Change summary.
    - Corresponding User Story (US).
    - Passed unit tests.

---

## Definition of Done (DoD)

1. Include unit tests.
2. It must not break existing unit tests.
3. It must comply with the defined coding conventions (PEP 8).
4. It must solve the associated User Story (US).

---

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- pytest (optional for unit tests)

---

## EPIC: User Management

### Epic ID

`LS-GTT-001` - Log-in and Sign-up Interface

### Epic Structure Breakdown

- **Epic Prefix:** Select an Epic label.
- **Functionality Code (2 Letters):** LS (Log-in / Sign-up)
- **Team ID:** 
   - GTT - Grupo Front-Tera  
   - CHK - CHIKI  
   - LCS - Los Crudos  
   - TDS - Tronaditas🔥
   - AIA - Agentes IA
- **Component Assignment:**
  - `001` - User Management
  - `002` - Search and Selection of Tutorials
  - `003` - Session Scheduling and Management
  - `004` - Tutorial Interaction and Development
  - `005` - Administrative Management and Moderation
  - `006` - Notifications and Follow-up

### Description

Log-in and Sign-up functionality for the system.

## User Stories

All user stories follow the **INVEST principles:** Independent, Negotiable, Valuable, Estimable, Small, Testable.

### User Story ID:
```
    LN-GTT-001 Log in interface
    ##-###-###-######
```

### User Story Structure Breakdown:
1. **User Story Prefix:** Select an US label.
2. **Functionality Code (2 Letters):** `LN` (Log-in)
3. **Epic and Component ID:**
   - 001 - User Management  
   - 002 - Search and Selection of Tutorials  
   - 003 - Session Scheduling and Management  
   - 004 - Tutorial Interaction and Development  
   - 005 - Administrative Management and Moderation  
   - 006 - Notifications and Follow-up
4. **Responsible Team:**
   - GTT - Grupo Front-Tera  
   - CHK - CHIKI  
   - LCS - Los Crudos  
   - TDS - Tronaditas🔥
   - AIA - Agentes IA


### User Story Format

```
As a [type of user]  
I want to [perform an action]  
So that [specific goal or benefit]  
```

### Example

```
As a user  
I want to register on the website  
So that I can access the website.  
```
---

## Acceptance Criteria

Each user story should have clearly defined acceptance criteria written in **Gherkin format** to specify the conditions for success. This ensures that the story is testable and meets the requirements.

### Format

- **Given** [Initial context]
- **When** [Action performed]
- **Then** [Expected outcome]

### Example (User Registration)

```
Scenario: Successful Registration

Given that the user is on the registration page  
When the user enters their full name, email address, password, and clicks on "Register"  
Then the system creates a new user account  
And redirects the user to the login page with a confirmation message.  
```

### Guidelines

- Include both positive and negative test cases.
- Be specific and define clear outcomes and conditions.
- Follow the "Given-When-Then" format.

---

## Artifacts

- **Prototypes:** Wireframes, Mockups, UI Design.
- **Personas:** Detailed user profiles.
- **Storyboards:** User flow diagrams.
- **Use Cases:** Detailed interaction descriptions.
- **Design Diagrams:** Class diagrams, sequence diagrams, architecture diagrams, etc.

---
## Story Points

Estimate the effort using the Fibonacci sequence: ?, 0, 0.5, 1, 2, 3, 5, 8, 13, 20, 100.

---

## Backlog: Priority & Risk ()

### Priority Levels

- Highest
- High
- Medium
- Low
- Lowest

### Risk Levels

- High
- Normal
- Low

### User Story Status

- New
- Not Started
- Assigned
- In Progress
- Ready for Test
- Done
- Accepted
- Canceled
- Postponed
- Blocked

---


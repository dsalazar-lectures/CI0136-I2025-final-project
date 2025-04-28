# How to Run Tests

This project includes unit tests to validate the user registration and authentication logic.

Follow these steps:

---

## 1. Install dependencies

Ensure you have your virtual environment activated.

Install `pytest` if it is not already installed:

```bash
pip install pytest
```

---

## 2. Navigate to the project directory

In the terminal, move to the root directory of the project:

Example:

```bash
cd CI0136-I2025-final-project
```

---

## 3. Run all tests

Execute:

```bash
pytest
```

This will discover and run all tests located inside the `tests/` folder.

---

## Notes

- Tests are implemented using `pytest`.
- Warnings about `werkzeug` or `ast` can be ignored, they are external to the project.
- All tests should pass without errors to ensure the system logic is working correctly.

---

# Example Output

```bash
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-8.3.5
collected 6 items

tests/test_registration_service.py ......                                     [100%]

============================== 6 passed in 0.23s ==============================
```

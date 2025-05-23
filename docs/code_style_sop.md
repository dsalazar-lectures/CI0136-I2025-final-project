# Code Style and Quality Checks SOP

## Overview
This document outlines the code style and quality checks implemented in our project using Flake8 and pre-commit hooks. These tools help maintain consistent code quality and style across the codebase.

## Tools Used
- Flake8: Main code style checker
- pre-commit: Git hook manager
- GitHub Actions: CI/CD pipeline integration

## Config Files
1. `.flake8`: Main Flake8 configuration
2. `.pre-commit-config.yaml`: Pre-commit hooks configuration
3. `.github/workflows/flake8.yml`: GitHub Actions workflow

## Code Style Rules

### 1. Line Length
- Maximum line length: 79 characters
- Docstrings and comments: 72 characters

### 2. Indentation
- Use 4 spaces for indentation
- No tabs allowed
- Maximum indentation level: 4 levels

### 3. Blank Lines
- Two blank lines before top-level functions and classes
- One blank line before method definitions in classes
- No more than two blank lines in a row

### 4. Imports
- Imports should be on separate lines
- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- No wildcard imports (`from module import *`)

### 5. Naming Conventions
- Class names: CapWords (PascalCase)
- Function and variable names: snake_case
- Constants: UPPER_CASE
- Private members: start with underscore

### 6. Comments
- Use complete sentences
- Start with a capital letter
- End with a period
- Two spaces before inline comments
- Block comments should start with '# '

### 7. String Formatting
- Use f-strings for string formatting
- Use single quotes for strings unless double quotes are needed

## Development Workflow

### 1. Initial Setup
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

### 2. Local Development
- Pre-commit hooks will run automatically before each commit
- To run checks manually:
```bash
# Check all files
pre-commit run --all-files

# Check specific files
pre-commit run --files path/to/file1.py path/to/file2.py
```

### 3. Handling Style Issues
When pre-commit finds issues:
1. Review the error messages in your terminal
2. Fix the issues in your code
3. Stage the changes
4. Try committing again

### 4. GitHub Integration
- GitHub Actions runs Flake8 on:
  - Every push to main/master
  - Every pull request
- Pull requests will be blocked if:
  - Style issues are found
  - The checks fail

## Common Issues and Solutions

### 1. Line Too Long
```python
# Bad
def process_user_data(user_id, user_name, user_email, user_phone_number, user_address, user_preferences):

# Good
def process_user_data(
    user_id,
    user_name,
    user_email,
    user_phone_number,
    user_address,
    user_preferences
):
```

### 2. Missing Blank Lines
```python
# Bad
class User:
    def __init__(self):
        pass
    def get_name(self):
        return self.name

# Good
class User:
    def __init__(self):
        pass

    def get_name(self):
        return self.name
```

### 3. Incorrect Naming
```python
# Bad
class userProfile:
    def GetName(self):
        return self.name

# Good
class UserProfile:
    def get_name(self):
        return self.name
```

## IDE Integration

### VS Code
1. Install Python extension
2. Enable Flake8 in settings:
```json
{
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true
}
```

### PyCharm
1. Go to Settings/Preferences
2. Navigate to Tools > External Tools
3. Add Flake8 as an external tool

## Troubleshooting

### Common Problems
1. Pre-commit not running:
   - Check if hooks are installed: `pre-commit --version`
   - Reinstall hooks: `pre-commit install`

2. False positives:
   - Add specific ignores in `.flake8`
   - Use `# noqa` comments for specific lines

3. Performance issues:
   - Exclude large directories in `.flake8`
   - Use `--files` to check specific files

## Maintenance

### Updating Dependencies
1. Update versions in `requirements.txt`
2. Update versions in `.pre-commit-config.yaml`
3. Run `pre-commit autoupdate`

### Adding New Rules
1. Add rules to `.flake8`
2. Update this SOP
3. Notify team members

## References
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [pre-commit Documentation](https://pre-commit.com/) 
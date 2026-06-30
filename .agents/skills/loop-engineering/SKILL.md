```markdown
# loop-engineering Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill provides guidance on the development patterns and workflows used in the `loop-engineering` Python codebase. It covers coding conventions, commit practices, testing patterns, and step-by-step instructions for maintaining CI workflows, particularly secret scanning. This is intended for contributors aiming for consistency and reliability in their contributions.

## Coding Conventions

### File Naming
- Use **snake_case** for all Python files.
  - Example: `data_processor.py`, `utils/helpers.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .utils import calculate_sum
    from ..models import DataModel
    ```

### Export Style
- Use **named exports** (explicitly listing what is exported in `__all__` if needed).
  - Example:
    ```python
    __all__ = ["calculate_sum", "DataModel"]
    ```

### Commit Message Style
- Follow the **conventional commit** format.
- Prefixes used: `fix`, `chore`
- Example:
  ```
  fix: correct calculation in data_processor
  chore: update dependencies for security
  ```

## Workflows

### Update Secret Scan Workflow
**Trigger:** When you need to change how secret scanning is performed or want to trigger a scan in the CI pipeline.  
**Command:** `/update-secret-scan`

1. Edit `.github/workflows/secret-scan.yml` to update configuration or trigger a run.
2. Commit your changes with a message referencing secret scan or gitleaks.
   - Example:
     ```
     chore: update secret scan workflow for new token pattern
     ```
3. Optionally, update related documentation or agent files if the workflow logic changes.
4. Push your changes and create a pull request if required.

**Files Involved:**
- `.github/workflows/secret-scan.yml`

## Testing Patterns

- **Test file naming:** Use `*.test.*` pattern for test files.
  - Example: `data_processor.test.py`
- **Testing framework:** Not explicitly detected; ensure tests are runnable via standard Python test runners (e.g., `pytest` or `unittest`).
- **Test location:** Place test files alongside the modules they test or in a dedicated `tests/` directory.

## Commands

| Command               | Purpose                                                        |
|-----------------------|----------------------------------------------------------------|
| /update-secret-scan   | Update or trigger the secret scanning workflow in CI           |
```

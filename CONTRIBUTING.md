# Contributing to AI Math Assistant

Thank you for your interest in contributing to the AI Math Assistant project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. We expect:

- **Respectful Communication**: Be kind and considerate in all interactions
- **Constructive Feedback**: Provide helpful, actionable feedback
- **Collaboration**: Work together to improve the project
- **Inclusivity**: Welcome contributors of all skill levels and backgrounds

## 🚀 Getting Started

1. **Fork the Repository**: Click the "Fork" button on GitHub
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/your-username/agentic-ai.git
   cd agentic-ai
   ```
3. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/agentic-ai.git
   ```
4. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💡 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix issues in existing code
- **New Features**: Add new tools or capabilities
- **Documentation**: Improve or expand documentation
- **Examples**: Add new examples or use cases
- **Tests**: Improve test coverage
- **Performance**: Optimize existing code
- **Tutorials**: Create educational content

### Areas for Contribution

1. **New Mathematical Tools**
   - Division operations
   - Advanced mathematical functions (logarithms, trigonometry)
   - Statistical operations
   - Matrix operations

2. **Enhanced Error Handling**
   - Input validation
   - Better error messages
   - Edge case handling

3. **Documentation**
   - API documentation
   - Tutorial improvements
   - Code examples
   - Video tutorials

4. **Testing**
   - Unit tests for tools
   - Integration tests for agents
   - Performance benchmarks

5. **LLM Integration**
   - Support for additional LLM providers
   - Model comparison utilities
   - Performance optimization

## 🛠️ Development Setup

### Prerequisites

- Python 3.13 or higher
- Git
- Jupyter Notebook/Lab
- Virtual environment tool (venv or conda)

### Setup Instructions

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Development Dependencies**:
   ```bash
   pip install pytest black flake8 mypy jupyter
   ```

4. **Verify Installation**:
   ```bash
   python -c "import langchain; print('LangChain installed successfully')"
   ```

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Naming Conventions**:
  - Functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
  - Private methods: `_leading_underscore`

### Code Formatting

Use `black` for automatic code formatting:

```bash
black your_file.py
```

### Linting

Run `flake8` to check code quality:

```bash
flake8 your_file.py
```

### Type Hints

Use type hints for function parameters and return values:

```python
def add_numbers(inputs: str) -> dict:
    """Add numbers from a string input."""
    # Implementation
    return {"result": sum}
```

### Documentation

#### Function Documentation

Use Google-style docstrings:

```python
def multiply_numbers(inputs: str) -> dict:
    """
    Multiplies a list of numbers from string input.

    Args:
        inputs (str): String containing numbers to multiply.

    Returns:
        dict: Dictionary with 'result' key containing the product.

    Example:
        >>> multiply_numbers("2 3 4")
        {'result': 24}

    Raises:
        ValueError: If no valid numbers are found in input.
    """
    # Implementation
```

#### Tool Documentation

When creating new tools, include:

1. **Clear Purpose**: What the tool does
2. **Input Format**: Expected input structure
3. **Output Format**: What the tool returns
4. **Examples**: Usage examples
5. **Error Cases**: How errors are handled

Example:

```python
from langchain.agents import Tool

def power_tool(inputs: str) -> dict:
    """
    Calculates the power of a base number raised to an exponent.
    
    Parameters:
        inputs (str): String containing base and exponent (e.g., "2 3" for 2^3)
    
    Returns:
        dict: Dictionary with 'result' key containing the power result
    
    Example:
        >>> power_tool("2 3")
        {'result': 8}
    """
    numbers = [int(x) for x in inputs.split() if x.isdigit()]
    if len(numbers) != 2:
        raise ValueError("Power tool requires exactly two numbers")
    return {"result": numbers[0] ** numbers[1]}

# Create the tool
power = Tool(
    name="PowerTool",
    func=power_tool,
    description="Calculates base raised to exponent power. Input: 'base exponent'"
)
```

## 🧪 Testing Guidelines

### Writing Tests

Create tests in the `tests/` directory:

```python
import pytest
from your_module import add_numbers

def test_add_numbers_basic():
    """Test basic addition functionality."""
    result = add_numbers("1 2 3")
    assert result == {"result": 6}

def test_add_numbers_with_text():
    """Test addition with non-numeric text."""
    result = add_numbers("add 10 and 20")
    assert result == {"result": 30}

def test_add_numbers_empty():
    """Test addition with no numbers."""
    result = add_numbers("no numbers here")
    assert result == {"result": 0}
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage
pytest --cov=your_module tests/
```

### Test Coverage

Aim for at least 80% code coverage for new features.

## 📤 Submitting Changes

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:

```
feat(tools): add division tool for mathematical operations

Implemented a new division tool that handles:
- Basic division operations
- Division by zero error handling
- Floating point results

Closes #123
```

```
fix(agent): resolve tool selection issue with complex queries

The agent was incorrectly selecting tools when queries contained
multiple operations. Updated the tool selection logic to properly
parse and prioritize operations.

Fixes #456
```

### Pull Request Process

1. **Update Your Branch**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push Your Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**:
   - Go to GitHub and create a PR from your fork
   - Fill out the PR template completely
   - Link related issues
   - Add appropriate labels

4. **PR Requirements**:
   - All tests must pass
   - Code must be formatted with `black`
   - No linting errors from `flake8`
   - Documentation updated if needed
   - Changelog updated for significant changes

5. **Review Process**:
   - Address reviewer feedback promptly
   - Make requested changes in new commits
   - Keep the PR focused on a single feature/fix

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated

## Related Issues
Closes #(issue number)
```

## 🐛 Reporting Issues

### Before Reporting

1. Check existing issues to avoid duplicates
2. Verify the issue with the latest version
3. Collect relevant information

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.13.5]
- LangChain Version: [e.g., 0.3.23]
- LLM Provider: [e.g., Ollama, OpenAI]

## Additional Context
Screenshots, logs, or other relevant information
```

## 💭 Feature Requests

We welcome feature requests! Please provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **Additional Context**: Examples, mockups, etc.

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)

## 🙋 Questions?

If you have questions about contributing:

1. Check the [documentation](docs/)
2. Review existing issues and discussions
3. Create a new discussion on GitHub
4. Reach out to maintainers

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to AI Math Assistant! Your efforts help make this project better for everyone.
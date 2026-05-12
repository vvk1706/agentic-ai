---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

Steps to reproduce the behavior:

1. Go to '...'
2. Execute '...'
3. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Error Messages

```
Paste any error messages or stack traces here
```

## Environment

**System Information:**
- OS: [e.g., Ubuntu 22.04, macOS 13.0, Windows 11]
- Python Version: [e.g., 3.13.5]
- Shell: [e.g., bash, zsh, PowerShell]

**Package Versions:**
- LangChain: [e.g., 0.3.23]
- LangChain-Ollama: [e.g., 0.3.0]
- LangChain-OpenAI: [e.g., 0.3.16]
- Other relevant packages: [list versions]

**LLM Provider:**
- [ ] Ollama (specify model: ___)
- [ ] OpenAI (specify model: ___)
- [ ] IBM watsonx (specify model: ___)
- [ ] Other: ___

## Code Sample

```python
# Minimal code sample that reproduces the issue
# Include imports and setup code

from langchain_ollama import ChatOllama
from langchain.agents import Tool

# Your code here
```

## Screenshots

If applicable, add screenshots to help explain your problem.

## Additional Context

Add any other context about the problem here. For example:
- Does this happen consistently or intermittently?
- Did this work in a previous version?
- Are there any workarounds you've found?

## Possible Solution

If you have suggestions on how to fix the bug, please describe them here.

## Checklist

- [ ] I have searched existing issues to ensure this is not a duplicate
- [ ] I have provided all requested information
- [ ] I have included a minimal code sample that reproduces the issue
- [ ] I have tested with the latest version of the dependencies
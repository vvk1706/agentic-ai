# Pull Request

## Description

Please include a summary of the changes and the related issue. Include relevant motivation and context.

Fixes #(issue)

## Type of Change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test addition or update
- [ ] Build/CI configuration change

## Changes Made

Please provide a detailed list of changes:

- Change 1
- Change 2
- Change 3

## Testing

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.

**Test Configuration:**
- OS: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.13.5]
- LLM Provider: [e.g., Ollama with llama3]

**Test Cases:**

1. Test case 1
   ```python
   # Code to reproduce test
   ```
   Expected result: ...
   Actual result: ...

2. Test case 2
   ```python
   # Code to reproduce test
   ```
   Expected result: ...
   Actual result: ...

## Checklist

### Code Quality

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have run `black` for code formatting
- [ ] I have run `flake8` and addressed any issues

### Documentation

- [ ] I have made corresponding changes to the documentation
- [ ] I have updated the README.md if needed
- [ ] I have added/updated docstrings for new/modified functions
- [ ] I have updated the CHANGELOG.md (if applicable)

### Testing

- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested with multiple LLM providers (if applicable)
- [ ] I have tested edge cases and error conditions

### Dependencies

- [ ] I have updated requirements.txt if I added new dependencies
- [ ] All new dependencies are necessary and well-justified
- [ ] I have verified compatibility with existing dependencies

## Screenshots (if applicable)

Add screenshots to help explain your changes.

## Breaking Changes

If this PR introduces breaking changes, please describe:

1. What breaks
2. Why it was necessary
3. Migration path for users

## Additional Notes

Add any additional notes, concerns, or questions here.

## Related Issues/PRs

- Related to #(issue)
- Depends on #(PR)
- Blocks #(issue)

## Reviewer Notes

Any specific areas you'd like reviewers to focus on?

---

**For Maintainers:**

- [ ] Code review completed
- [ ] Tests passing
- [ ] Documentation reviewed
- [ ] Ready to merge
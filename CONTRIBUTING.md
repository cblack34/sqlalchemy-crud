# Contributing to sqlalchemy-crud

Thank you for considering contributing to sqlalchemy-crud!
I appreciate your interest in making this library better.
By contributing, you enhance its features, fix issues, 
and improve overall code quality.

To contribute to sqlalchemy-crud, 
please follow the guidelines outlined in this document. 
By adhering to these guidelines, 
you ensure a smooth and efficient collaboration process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Formatting](#code-formatting)
- [Pull Requests](#pull-requests)
- [License](#license)

## Code of Conduct

We strive to maintain a friendly and inclusive community. 

## Reporting Issues

If you encounter any issues or bugs while using sqlalchemy-crud, please help us improve by reporting them. To report an issue:

1. Check the existing issues to ensure it hasn't already been reported.
2. Create a new issue, providing a clear and descriptive title.
3. Describe the issue in detail, including steps to reproduce it, if applicable.
4. Include any relevant error messages or screenshots.

## Feature Requests

We welcome feature requests that can enhance sqlalchemy-crud. To submit a feature request:

1. Check the existing feature requests to avoid duplicates.
2. Create a new feature request, providing a concise and descriptive title.
3. Clearly explain the proposed feature and its potential benefits.

## Development Setup

To set up sqlalchemy-crud for local development, follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Install the project dependencies using `poetry install --no-root --with=dev`.
5. Create a new branch for your changes: `git checkout -b my-feature-branch`.

## Making Changes

When making changes to the sqlalchemy-crud library, please keep the following guidelines in mind:

1. Follow the existing code style and conventions.
2. Write clear and concise commit messages.
3. Keep each commit focused on a specific change or improvement.
4. Test your changes thoroughly before submitting a pull request.
5. Document any new features, modifications, or additions.

## Testing

We maintain a comprehensive test suite for sqlalchemy-crud to ensure its stability and reliability. Before submitting your changes, please run the tests locally using the command `poetry run pytest`. Make sure all existing tests pass and consider adding new tests for the changes you made, if applicable.

## Code Formatting

> you can have any color you want as long as it's black

We use the [black](https://github.com/psf/black) code formatter to maintain consistent code style throughout the project. To format your code, run `poetry run black .` in the project's root directory. Ensure that your changes conform to the formatting guidelines.

## Pull Requests

When you're ready to contribute your changes, submit a pull request (PR) to the main repository. Please include the following information in your PR:

1. A clear and descriptive title.
2. Detailed description of the changes made.
3. Reference any related issues or feature requests.
4. Ensure that all tests pass.
5. Make sure the code is properly formatted.

I will review your PR, provide feedback, 
and work with you to address any necessary changes. 
Once approved, I'll merge your changes into the main repository.

## License

By contributing to sqlalchemy-crud, 
you agree that your contributions will be licensed under 
the [MIT License](LICENSE).

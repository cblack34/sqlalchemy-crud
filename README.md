# SQLAlchemy Crud

[![.github/workflows/poetry-pytest.yml](https://github.com/cblack34/sqlalchemy-crud/actions/workflows/poetry-pytest.yml/badge.svg?event=push)](https://github.com/cblack34/sqlalchemy-crud/actions/workflows/poetry-pytest.yml)
[![codecov](https://codecov.io/gh/cblack34/sqlalchemy-crud/branch/master/graph/badge.svg?token=230RWC83HD)](https://codecov.io/gh/cblack34/sqlalchemy-crud)


sqlalchemy-crud is a Python library that takes the pain out of performing common CRUD operations on SQLAlchemy models. It provides a simple and intuitive interface to create, read, update, and delete records in your database.

## Table of Contents

- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Testing](#testing)
- [Compatibility](#compatibility)
- [License](#license)
- [Versioning](#versioning)
- [Authors and Acknowledgments](#authors-and-acknowledgments)

## Installation

You can easily install sqlalchemy-crud using Poetry, a dependency management tool for Python:

```shell
$ poetry add sqlalchemy-crud
```

Make sure you have Python 3.8, 3.9, 3.10, or 3.11 installed.

## Usage Examples

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_crud import crud

from my_app.models import MyModel

# Set up the SQLAlchemy session
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
db = Session()

# Create a new object
model = crud.create_model(db, MyModel, schema={"name": "John Doe"})

# Retrieve all objects
models = crud.get_models(db, MyModel)

# Retrieve an object by ID
model = crud.get_model(db, MyModel, model_id=1)

# Retrieve objects by a specific attribute
models = crud.get_models_by_attribute(db, MyModel, attribute="name", value="John Doe")
model = crud.get_model_by_attribute(db, MyModel, attribute="uuid", value="123e4567-e89b-12d3-a456-426614174000")

# Update an object
model = crud.update_model(db, MyModel, model_id=1, schema={"name": "Jane Doe"})

# Delete an object
crud.delete_model(db, MyModel, model_id=1)
```

## Getting Started

To get started with sqlalchemy-crud, follow these steps:

1. Install the library using the instructions provided in the [Installation](#installation) section.
2. Import the necessary modules and create a SQLAlchemy session.
3. Use the CRUD functions (`create_model`, `get_model`, `update_model`, `delete_model`, etc.) to perform operations on your SQLAlchemy models.
4. Refer to the [Usage Examples](#usage-examples) section for more detailed examples and code snippets.

## Contributing

I welcome contributions from the community! If you'd like to contribute to sqlalchemy-crud, please follow the guidelines outlined in [CONTRIBUTING.md](https://example.com/contributing).

## Testing

To run the tests for sqlalchemy-crud, execute the following command:

```shell
$ poetry run pytest
```

[//]: # (## Code Quality)

[//]: # ()
[//]: # (The library adheres to high code quality standards. We use black for code formatting, pylint for static analysis, and pytest-cov for code coverage. To ensure code quality, run the following command:)

[//]: # ()
[//]: # (```shell)

[//]: # ($ poetry run pylint sqlalchemy_crud tests)

[//]: # (```)

## Compatibility

sqlalchemy-crud is compatible with Python 3.8, 3.9, 3.10, and 3.11. 
It works with SQLAlchemy 1.3.19 up to but excluding (<) 2.

## License

This library is released under the MIT License. See the [LICENSE](https://example.com/license) file for more details.

## Versioning

this project follows semantic versioning for sqlalchemy-crud releases.

## Authors and Acknowledgments

sqlalchemy-crud is maintained by Clayton Black. 

Thank you to all the contributors to open-source software.  
Not only do I use a lot of it, but I learn a lot from it as well.

I hope you find sqlalchemy-crud useful in your projects and appreciate your feedback and contributions!

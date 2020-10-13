import time

import pytest

from sqlalchemy_crud.tests.test_database import setup_database
from sqlalchemy_crud import crud
from sqlalchemy_crud.tests import test_models

parent_1 = {"name": "John"}
parent_2 = {"name": "Paul"}
parent_2 = {"name": "Mary"}

bad_parent_1 = {"invalid_field": "That's not what your mom said."}

child = {"name": "Mike"}


def test_create_get_model(setup_database):
    db = setup_database

    created_parent: test_models.Parent = crud.create_model(
        db, test_models.Parent, parent_1
    )
    db_parent: test_models.Parent = crud.get_model(
        db, test_models.Parent, created_parent.id
    )

    # time.sleep(100)

    assert parent_1["name"] == db_parent.name


def test_create_raise_exception_on_invalid_attribute(setup_database):
    db = setup_database

    with pytest.raises(TypeError) as excinfo:
        crud.create_model(db, test_models.Parent, bad_parent_1)


def test_update_model(setup_database):
    db = setup_database

    # Create parent at John
    created_parent = crud.create_model(db, test_models.Parent, parent_1)

    # Update parent from John -> Paul
    crud.update_model(db, test_models.Parent, created_parent.id, parent_2)

    # Get parent from db
    db_parent: test_models.Parent = crud.get_model(
        db, test_models.Parent, created_parent.id
    )

    assert parent_2["name"] == db_parent.name


def test_update_raise_exception_on_invalid_attribute(setup_database):
    db = setup_database

    # Create parent at John
    created_parent = crud.create_model(db, test_models.Parent, parent_1)

    with pytest.raises(TypeError) as excinfo:
        # Update parent with invalid field
        crud.update_model(db, test_models.Parent, created_parent.id, bad_parent_1)
import pytest

from sqlalchemy_crud.tests.test_database import setup_database  # noqa: F401
from sqlalchemy_crud import crud
from sqlalchemy_crud.tests import test_models

parents = {1: {"name": "John"}, 2: {"name": "Paul"}, 3: {"name": "Mary"}}

bad_parents = {1: {"invalid_field": "That's not what your mom said."}}

children = {1: {"name": "Mike"}}


def test_create_get_model(setup_database):  # noqa: F811
    db = setup_database

    for parent in parents:
        created_parent: test_models.Parent = crud.create_model(
            db, test_models.Parent, parents[parent]
        )
        db_parent: test_models.Parent = crud.get_model(
            db, test_models.Parent, created_parent.id
        )

        assert parents[parent]["name"] == db_parent.name

    db_parents = crud.get_models(db, test_models.Parent)
    for parent in db_parents:
        assert parents[parent.id]["name"] == parent.name


def test_create_raise_exception_on_invalid_attribute(setup_database):  # noqa: F811
    db = setup_database

    with pytest.raises(TypeError):
        crud.create_model(db, test_models.Parent, bad_parents[1])


def test_update_model(setup_database):  # noqa: F811
    db = setup_database

    # Create parents at John
    created_parent = crud.create_model(db, test_models.Parent, parents[1])

    # Update parents from John -> Paul
    crud.update_model(db, test_models.Parent, created_parent.id, parents[2])

    # Get parents from db
    db_parent: test_models.Parent = crud.get_model(
        db, test_models.Parent, created_parent.id
    )

    assert parents[2]["name"] == db_parent.name


def test_update_raise_exception_on_invalid_attribute(setup_database):  # noqa: F811
    db = setup_database

    # Create parents at John
    created_parent = crud.create_model(db, test_models.Parent, parents[1])

    with pytest.raises(TypeError):
        # Update parents with invalid field
        crud.update_model(db, test_models.Parent, created_parent.id, bad_parents[1])


def test_delete_model(setup_database):  # noqa: F811
    db = setup_database

    # Create parents at John
    created_parent = crud.create_model(db, test_models.Parent, parents[1])

    assert crud.delete_model(db, test_models.Parent, created_parent.id) is None


def test_delete_nonexistent_model(setup_database):  # noqa: F811
    from sqlalchemy.orm.exc import UnmappedInstanceError

    db = setup_database

    with pytest.raises(UnmappedInstanceError):
        crud.delete_model(db, test_models.Parent, 500)


def test_get_nonexistent_model(setup_database):  # noqa: F811
    db = setup_database
    db_parent = crud.get_model(db, test_models.Parent, 500)

    assert db_parent is None


def test_get_model_by_attribute(setup_database):  # noqa: F811
    db = setup_database

    # Create parents at John
    created_parent = crud.create_model(db, test_models.Parent, parents[1])

    db_parent = crud.get_model_by_attribute(
        db, test_models.Parent, "name", parents[1]["name"]
    )
    assert db_parent.id == created_parent.id
    assert db_parent.name == created_parent.name


def test_get_models_by_attribute(setup_database):  # noqa: F811
    db = setup_database

    # Create 3 parents 2 with the same name
    crud.create_model(db, test_models.Parent, parents[1])
    crud.create_model(db, test_models.Parent, parents[1])
    crud.create_model(db, test_models.Parent, parents[2])

    db_parents = crud.get_models_by_attribute(
        db, test_models.Parent, "name", parents[1]["name"]
    )

    assert len(db_parents) == 2
    assert db_parents[0].name == parents[1]["name"]
    assert db_parents[1].name == parents[1]["name"]


def test_link_and_unlink_models(setup_database):  # noqa: F811
    db = setup_database

    # Create a parent and a child
    created_parent = crud.create_model(db, test_models.Parent, parents[1])
    created_child = crud.create_model(db, test_models.Child, children[1])

    # Link the parent and child
    crud.link_models(
        db,
        test_models.Parent,
        created_parent.id,
        test_models.Child,
        created_child.id,
        "children",
    )

    db_parent = crud.get_model(db, test_models.Parent, created_parent.id)

    assert len(db_parent.children) == 1
    for child in db_parent.children:
        assert child.name == children[1]["name"]

    # Unlink the parent and child
    crud.unlink_models(
        db,
        test_models.Parent,
        created_parent.id,
        test_models.Child,
        created_child.id,
        "children",
    )

    assert len(db_parent.children) == 0

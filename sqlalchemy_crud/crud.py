"""
SQLAlchemy_CRUD

A functional module to help reduce the amount of boilerplate code
needed to deal with C.R.U.D. operations on a SQL db.

"""
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_models(
    db: Session, model: Base, offset: int = 0, limit: int = 100
) -> List[Base]:
    """
    Given a sqlalchemy Session and Model(Base) will return a list of Model(Base)


    :param db:
    :param model:
    :param offset: Used for paging. The starting row number. Defaults to 0
    :param limit: Used for paging. The number of rows to return. Defaults to 100.
    :return:
    """
    return db.query(model).offset(offset).limit(limit).all()


def get_model(db: Session, model: Base, model_id: int) -> Base:
    """
    Given a sqlalchemy Session, Model(Base), and ID
    will return a row from the data base as a Model(Base) or None if a row does not exist.

    :param db:
    :param model:
    :param model_id:
    :return:
    """
    return get_model_by_attribute(
        db=db, model=model, attribute="id", attribute_value=model_id
    )


def get_model_by_attribute(
    db: Session, model: Base, attribute: str, attribute_value
) -> Base:
    """
    Search a database table for a row with the attribute and value given

    :param db:
    :param model:
    :param attribute:
    :param attribute_value:
    :return:
    """
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return db.query(model).filter(model_attribute == attribute_value).first()

    raise AttributeError


def get_models_by_attribute(
    db: Session,
    model: Base,
    attribute: str,
    attribute_value,
    offset: int = 0,
    limit: int = 100,
) -> List[Base]:
    """
    Search a database table for all row with the given attribute value.

    :param db:
    :param model:
    :param attribute:
    :param attribute_value:
    :param offset:
    :param limit:
    :return:
    """
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return (
            db.query(model)
            .filter(model_attribute == attribute_value)
            .offset(offset)
            .limit(limit)
            .all()
        )

    raise AttributeError


def create_model(db: Session, model: Base, schema: dict) -> Base:
    """
    Create a row in a database table

    :param db:
    :param model:
    :param schema: schema is the wrong word, but this started off life as a FastAPI util
                   using pydantic models which I called schema
                   to keep separate from sqlachemy models.
    :return:
    """
    db_model = model(**schema)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def update_model(db: Session, model: Base, model_id: int, schema: dict) -> Base:
    """
    Update a row in a database table

    :param db:
    :param model:
    :param model_id:
    :param schema: See note on create_model
    :return:
    """
    db_model = get_model(db=db, model=model, model_id=model_id)
    for key, value in schema.items():
        if hasattr(db_model, key):
            setattr(db_model, key, value)
        else:
            raise TypeError(
                "%r is an invalid keyword argument for %s" % (key, type(db_model))
            )

    db.commit()
    db.refresh(db_model)
    return db_model


def delete_model(db: Session, model: Base, model_id: int) -> None:
    """
    Delete a row in a database table

    :param db:
    :param model:
    :param model_id:
    """
    db_model = get_model(db=db, model=model, model_id=model_id)
    db.delete(db_model)
    db.commit()


def link_models(
    db: Session,
    parent_model: Base,
    parent_id: int,
    child_model: Base,
    child_id: int,
    backref: str,
) -> Base:
    """
    Create relationships between rows in database tables to allow M:N relationships

    :param db:
    :param parent_model:
    :param parent_id:
    :param child_model:
    :param child_id:
    :param backref:
    :return:
    """
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).append(child)
        db.commit()
        db.refresh(parent)
        return parent

    raise AttributeError


def unlink_models(
    db: Session,
    parent_model: Base,
    parent_id: int,
    child_model: Base,
    child_id: int,
    backref: str,
) -> Base:
    """
    Remove relationships (M:N) between rows in database tables.

    :param db:
    :param parent_model:
    :param parent_id:
    :param child_model:
    :param child_id:
    :param backref:
    :return:
    """
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).remove(child)
        db.commit()
        db.refresh(parent)
        return parent

    raise AttributeError

from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


def get_models(
    db: Session, model: Base, offset: int = 0, limit: int = 100
) -> List[Base]:
    return db.query(model).offset(offset).limit(limit).all()


def get_model(db: Session, model: Base, model_id: int) -> Base:
    return get_model_by_attribute(
        db=db, model=model, attribute="id", attribute_value=model_id
    )


def get_model_by_attribute(
    db: Session, model: Base, attribute: str, attribute_value
) -> Base:
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return db.query(model).filter(model_attribute == attribute_value).first()
    else:
        raise AttributeError


def get_models_by_attribute(
    db: Session,
    model: Base,
    attribute: str,
    attribute_value,
    offset: int = 0,
    limit: int = 100,
) -> List[Base]:
    if hasattr(model, attribute):
        model_attribute = getattr(model, attribute)
        return (
            db.query(model)
            .filter(model_attribute == attribute_value)
            .offset(offset)
            .limit(limit)
            .all()
        )
    else:
        raise AttributeError


def create_model(db: Session, model: Base, schema: dict) -> Base:
    db_model = model(**schema)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def update_model(db: Session, model: Base, model_id: int, schema: dict) -> Base:
    db_model = get_model(db=db, model=model, model_id=model_id)
    for key, value in schema.items():
        if hasattr(db_model, key):
            setattr(db_model, key, value)
        else:
            raise AttributeError

    db.commit()
    db.refresh(db_model)
    return db_model


def delete_model(db: Session, model: Base, model_id: int) -> None:
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
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).append(child)
        db.commit()
        db.refresh(parent)
        return parent
    else:
        raise AttributeError


def unlink_models(
    db: Session,
    parent_model: Base,
    parent_id: int,
    child_model: Base,
    child_id: int,
    backref: str,
) -> Base:
    parent = get_model(db=db, model=parent_model, model_id=parent_id)
    child = get_model(db=db, model=child_model, model_id=child_id)

    if hasattr(parent, backref):
        getattr(parent, backref).remove(child)
        db.commit()
        db.refresh(parent)
        return parent
    else:
        raise AttributeError

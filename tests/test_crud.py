import unittest

import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy_crud.crud import (
    get_models,
    get_model,
    get_model_by_attribute,
    get_models_by_attribute, create_model, update_model,
    delete_model, link_models, unlink_models,
)
from tests.models_for_test import Base, Parent, Child


class TestGetModels(unittest.TestCase):
    def setUp(self):
        # create an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        session = sessionmaker(bind=engine)
        self.db = session()

        Base.metadata.create_all(engine)

    def tearDown(self):
        # remove test da
        Base.metadata.drop_all(self.db.bind)

    def create_test_data(self):
        for i in range(1, 101):
            self.db.add(Parent(name=f"parent_test_name_{i}", id_modulo=i % 10))

        for j in range(1, 201):
            self.db.add(Child(name=f"child_test_name_{j}"))

        self.db.commit()

    def link_children_to_parents(self):
        for i in range(1, 101):
            parent = (
                self.db.query(Parent)
                .filter(Parent.name == f"parent_test_name_{i}")
                .first()
            )

            # link 2 children to each parent
            child_1 = (
                self.db.query(Child)
                .filter(Child.name == f"child_test_name_{(2 * i) - 1}")
                .first()
            )
            child_2 = (
                self.db.query(Child)
                .filter(Child.name == f"child_test_name_{2 * i}")
                .first()
            )

            parent.children.append(child_1)
            parent.children.append(child_2)

        self.db.commit()

    def test_get_models_with_default_offset_and_limit(self):
        self.create_test_data()

        models = get_models(self.db, Parent)
        self.assertEqual(len(models), 100)
        self.assertEqual(models[0].name, "parent_test_name_1")
        self.assertEqual(models[-1].name, "parent_test_name_100")

    def test_get_models_with_custom_offset_and_limit(self):
        self.create_test_data()

        models = get_models(self.db, Parent, offset=50, limit=10)
        self.assertEqual(len(models), 10)
        self.assertEqual(models[0].name, "parent_test_name_51")
        self.assertEqual(models[-1].name, "parent_test_name_60")

    def test_get_models_with_relationship(self):
        self.create_test_data()
        self.link_children_to_parents()

        models = get_models(self.db, Parent)
        self.assertEqual(len(models), 100)
        self.assertEqual(len(models[0].children), 2)
        self.assertEqual(models[0].children[0].name, "child_test_name_1")
        self.assertEqual(models[0].children[1].name, "child_test_name_2")

        models = get_models(self.db, Parent, offset=50, limit=10)
        self.assertEqual(len(models), 10)
        self.assertEqual(len(models[0].children), 2)
        self.assertEqual(models[0].children[0].name, "child_test_name_101")
        self.assertEqual(models[0].children[1].name, "child_test_name_102")

    def test_get_model(self):
        self.create_test_data()

        model = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model.name, "parent_test_name_1")

        model = get_model(self.db, Parent, model_id=100)
        self.assertEqual(model.name, "parent_test_name_100")

        model = get_model(self.db, Parent, model_id=101)
        self.assertEqual(model, None)

    def test_get_model_with_relationship(self):
        self.create_test_data()
        self.link_children_to_parents()

        model = get_model(
            db=self.db,
            model=Parent,
            model_id=1,
        )
        self.assertEqual(len(model.children), 2)
        self.assertEqual(model.children[0].name, "child_test_name_1")
        self.assertEqual(model.children[1].name, "child_test_name_2")

        model: Parent = get_model(db=self.db, model=Parent, model_id=100)
        self.assertEqual(len(model.children), 2)
        self.assertEqual(model.children[0].name, "child_test_name_199")
        self.assertEqual(model.children[1].name, "child_test_name_200")

        model = get_model(db=self.db, model=Parent, model_id=101)
        self.assertEqual(model, None)

    def test_get_model_by_attribute(self):
        self.create_test_data()
        self.link_children_to_parents()

        model = get_model_by_attribute(
            db=self.db,
            model=Parent,
            attribute="name",
            attribute_value="parent_test_name_1",
        )
        self.assertEqual(model.name, "parent_test_name_1")
        self.assertEqual(model.id, 1)
        self.assertEqual(len(model.children), 2)

        model = get_model_by_attribute(
            db=self.db,
            model=Parent,
            attribute="name",
            attribute_value="parent_test_name_100",
        )
        self.assertEqual(model.name, "parent_test_name_100")
        self.assertEqual(model.id, 100)
        self.assertEqual(len(model.children), 2)

        model = get_model_by_attribute(
            db=self.db,
            model=Parent,
            attribute="name",
            attribute_value="parent_test_name_101",
        )
        self.assertEqual(model, None)

    def test_get_model_by_attribute_with_invalid_attribute(self):
        self.create_test_data()
        self.link_children_to_parents()

        with self.assertRaises(AttributeError):
            model = get_model_by_attribute(
                db=self.db,
                model=Parent,
                attribute="invalid_attribute",
                attribute_value="parent_test_name_1",
            )



    def test_get_models_by_attribute(self):
        self.create_test_data()
        self.link_children_to_parents()

        models = get_models_by_attribute(
            db=self.db, model=Parent, attribute="id_modulo", attribute_value=0
        )
        self.assertEqual(len(models), 10)
        self.assertEqual(models[0].name, "parent_test_name_10")
        self.assertEqual(models[-1].name, "parent_test_name_100")
        self.assertEqual(models[0].children[0].name, "child_test_name_19")
        self.assertEqual(models[-1].children[0].name, "child_test_name_199")

        models = get_models_by_attribute(
            db=self.db, model=Parent, attribute="id_modulo", attribute_value=1
        )
        self.assertEqual(len(models), 10)
        self.assertEqual(models[0].name, "parent_test_name_1")
        self.assertEqual(models[-1].name, "parent_test_name_91")
        self.assertEqual(models[0].children[0].name, "child_test_name_1")
        self.assertEqual(models[-1].children[0].name, "child_test_name_181")

        models = get_models_by_attribute(
            db=self.db, model=Parent, attribute="id_modulo", attribute_value=9
        )
        self.assertEqual(len(models), 10)
        self.assertEqual(models[0].name, "parent_test_name_9")
        self.assertEqual(models[-1].name, "parent_test_name_99")
        self.assertEqual(models[0].children[0].name, "child_test_name_17")
        self.assertEqual(models[-1].children[0].name, "child_test_name_197")

    def test_get_models_by_attribute_with_invalid_attribute(self):
        self.create_test_data()
        self.link_children_to_parents()

        with self.assertRaises(AttributeError):
            models = get_models_by_attribute(
                db=self.db,
                model=Parent,
                attribute="invalid_attribute",
                attribute_value="parent_test_name_1",
            )

    def test_create_model(self):
        model = create_model(
            db=self.db,
            model=Parent,
            schema=dict(name="parent_test_name_1", id_modulo=1),
        )
        self.assertEqual(model.name, "parent_test_name_1")
        self.assertEqual(model.id, 1)

        model_check = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model_check.name, "parent_test_name_1")
        self.assertEqual(model_check.id, 1)

        model = create_model(
            db=self.db,
            model=Parent,
            schema=dict(name="parent_test_name_2", id_modulo=2),
        )
        self.assertEqual(model.name, "parent_test_name_2")
        self.assertEqual(model.id, 2)

        model_check = get_model(db=self.db, model=Parent, model_id=2)
        self.assertEqual(model_check.name, "parent_test_name_2")
        self.assertEqual(model_check.id, 2)

    def test_create_model_raise_exception_on_invalid_attribute(self):
        with self.assertRaises(TypeError):
            create_model(
                db=self.db,
                model=Parent,
                schema=dict(name="parent_test_name_1", id_modulo=1, invalid=1),
            )

    def test_update_model(self):
        self.create_test_data()
        self.link_children_to_parents()

        model = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model.name, "parent_test_name_1")

        model = update_model(
            db=self.db,
            model=Parent,
            model_id=1,
            schema=dict(name="parent_test_name_1_updated"),
        )
        self.assertEqual(model.name, "parent_test_name_1_updated")

        model = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model.name, "parent_test_name_1_updated")

    def test_update_model_raise_exception_on_invalid_attribute(self):
        with self.assertRaises(AttributeError):
            update_model(
                db=self.db,
                model=Parent,
                model_id=1,
                schema=dict(name="parent_test_name_1_updated", invalid=1),
            )

    def test_delete_model(self):
        self.create_test_data()
        self.link_children_to_parents()

        model = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model.name, "parent_test_name_1")

        delete_model(db=self.db, model=Parent, model_id=1)

        model = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(model, None)

    def test_link_models(self):
        """
        Test linking models

        @todo: Change link_models to accept an instance of a model instead of a model class or maybe both
        :return:
        """
        self.create_test_data()

        link_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1, backref="children")
        link_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=2, backref="children")

        parent = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(parent.name, "parent_test_name_1")
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].name, "child_test_name_1")
        self.assertEqual(parent.children[1].name, "child_test_name_2")

        child = get_model(db=self.db, model=Child, model_id=1)
        self.assertEqual(child.name, "child_test_name_1")
        self.assertEqual(child.parents[0].id, 1)

        child = get_model(db=self.db, model=Child, model_id=2)
        self.assertEqual(child.name, "child_test_name_2")
        self.assertEqual(child.parents[0].id, 1)

    def test_link_models_raise_exception_on_invalid_backref_attribute(self):
        self.create_test_data()

        with self.assertRaises(AttributeError):
            link_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1, backref="invalid")

    def test_link_models_raise_exception_on_invalid_parent_id(self):
        """
        Test linking models
        @todo: Make link_models raise an exception if the parent_id is invalid
        :return:
        """
        self.create_test_data()

        with self.assertRaises(AttributeError):
            link_models(db=self.db, parent_model=Parent, parent_id=1000, child_model=Child, child_id=1, backref="children")

    def test_link_models_raise_exception_on_invalid_child_id(self):
        """
        Test linking models
        """
        pytest.skip("Not implemented yet")
        self.create_test_data()

        with self.assertRaises(AttributeError):
            link_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1000, backref="children")

    def test_unlink_models(self):
        """
        Test unlinking models
        @todo: Change unlink_models to accept an instance of a model instead of a model class or maybe both.
            The child should accept either. or we could make a new functions for unlinking models by id and by model instance.
        @todo: Make unlink_models accept a list of child ids or models.
        """
        self.create_test_data()
        self.link_children_to_parents()

        parent = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(len(parent.children), 2)

        unlink_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1, backref="children")

        parent = get_model(db=self.db, model=Parent, model_id=1)
        self.assertEqual(len(parent.children), 1)

    def test_unlink_models_raise_exception_on_invalid_backref_attribute(self):
        self.create_test_data()

        with self.assertRaises(AttributeError):
            unlink_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1, backref="invalid")

    def test_unlink_models_raise_exception_on_invalid_parent_id(self):
        """
        Test unlinking models
        @todo: Make unlink_models raise an exception if the parent_id is invalid
        """
        self.create_test_data()

        with self.assertRaises(AttributeError):
            unlink_models(db=self.db, parent_model=Parent, parent_id=1000, child_model=Child, child_id=1, backref="children")

    def test_unlink_models_raise_exception_on_invalid_child_id(self):
        """
        Test unlinking models
        """
        pytest.skip("Not implemented yet")
        self.create_test_data()

        with self.assertRaises(AttributeError):
            unlink_models(db=self.db, parent_model=Parent, parent_id=1, child_model=Child, child_id=1000, backref="children")


if __name__ == "__main__":
    unittest.main()

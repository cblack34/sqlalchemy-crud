import unittest

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy_crud.crud import get_models
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
            self.db.add(Parent(name=f"parent_test_name_{i}"))

        for j in range(1, 201):
            self.db.add(Child(name=f"child_test_name_{j}"))

        self.db.commit()

    def link_children_to_parents(self):
        for i in range(1, 100):
            parent = (
                self.db.query(Parent)
                .filter(Parent.name == f"parent_test_name_{i}")
                .first()
            )

            # link 2 children to each parent
            child_1 = (
                self.db.query(Child)
                .filter(Child.name == f"child_test_name_{(2*i)-1}")
                .first()
            )
            child_2 = (
                self.db.query(Child)
                .filter(Child.name == f"child_test_name_{2*i}")
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


if __name__ == "__main__":
    unittest.main()

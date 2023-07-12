import unittest

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy_crud.crud import Base, get_models


# create models for testing
class TestModel(Base):
    __tablename__ = 'test_models'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class TestGetModels(unittest.TestCase):
    def setUp(self):
        # create an in-memory SQLite database for testing
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.db = Session()

        Base.metadata.create_all(engine)

        # add some test data to the database
        for i in range(1, 101):
            test_model = TestModel(id=i, name=f'test_name_{i}')
            self.db.add(test_model)
        self.db.commit()

    def test_get_models_with_default_offset_and_limit(self):
        models = get_models(self.db, TestModel)
        self.assertEqual(len(models), 100)
        self.assertEqual(models[0].name, 'test_name_1')
        self.assertEqual(models[-1].name, 'test_name_100')

    def test_get_models_with_custom_offset_and_limit(self):
        models = get_models(self.db, TestModel, offset=50, limit=10)
        self.assertEqual(len(models), 10)
        self.assertEqual(models[0].name, 'test_name_51')
        self.assertEqual(models[-1].name, 'test_name_60')


if __name__ == '__main__':
    unittest.main()

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('Test')
        self.assertListEqual([], store.items.all(),
                             "Store should be empty we just initialized it")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test')
            self.assertIsNone(StoreModel.find_by_name('Test'),
                              "Stores should be empty befre saving any stores")
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('Test'),
                                 "Saving failed")

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('Test'),
                              "Deletion failed")

    def test_json(self):
        store = StoreModel('Test')
        expected = {'name': 'Test', 'items': []}
        self.assertEqual(store.json(), expected,
                         "Saving store items not matching expected")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name,  'test_item')


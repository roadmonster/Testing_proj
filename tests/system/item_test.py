import json

from tests.base_test import BaseTest
from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(auth_request.data)['access_token'])

    def test_get_item_without_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('costco').save_to_db()
                ItemModel('test item', 3.99, 1).save_to_db()
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_with_auth_no_item(self):
        with self.app() as client:
            resp = client.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(404, resp.status_code)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Costco').save_to_db()
                self.assertIsNone(ItemModel.find_by_name('toy_car'))
                resp = client.post('/item/toy_car', json={'name': 'toy_car', 'price': 7.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('toy_car'))
                self.assertEqual(ItemModel.find_by_name('toy_car').price, 7.99)

                self.assertDictEqual({'name': 'toy_car', 'price': 7.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Costco').save_to_db()
                self.assertIsNone(ItemModel.find_by_name('toy_car'))
                client.post('/item/toy_car', json={'name': 'toy_car', 'price': 7.99, 'store_id': 1})
                resp = client.post('/item/toy_car', json={'name': 'toy_car', 'price': 7.99, 'store_id': 1})
                self.assertDictEqual({'message': "An item with name 'toy_car' already exists."}, json.loads(resp.data))
                self.assertEqual(400, resp.status_code)

    def test_get_with_auth_item_exists(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 21.99, 1).save_to_db()
                resp = client.get('/item/test_item', headers={'Authorization': self.auth_header})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test_item', 'price': 21.99}, json.loads(resp.data))

    def test_delete_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 21.99, 1).save_to_db()
                resp = client.delete('/item/test_item')
                self.assertEqual(401, resp.status_code)

    def test_delete_item_with_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 21.99, 1).save_to_db()
                resp = client.delete('/item/test_item', headers={'Authorization': self.auth_header})
                self.assertEqual(200, resp.status_code)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', 21.99, 1).save_to_db()
                resp = client.put('/item/test_item', json={'name':'test_item', 'price': 2.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name':'test_item', 'price':2.99})

    def test_item_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/items')

                self.assertDictEqual(d1={'items': [{'name': 'test', 'price': 17.99}]},
                                     d2=json.loads(r.data))
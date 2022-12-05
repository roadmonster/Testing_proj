from tests.base_test import BaseTest
from models.user import UserModel

class UserTest(BaseTest):
    def test_create_user(self):
        with self.app_context():
            user = UserModel('test user', 'test password')
            self.assertIsNone(UserModel.find_by_username('test user'))

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username('test user'))
            self.assertIsNotNone(UserModel.find_by_id(1))
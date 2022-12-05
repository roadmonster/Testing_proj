from tests.unit.models.unit_base_test import UnitBaseTest
from models.user import UserModel
class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test user', 'test password')
        self.assertEqual(user.username, 'test user', 'Created user username different from expected')
        self.assertEqual(user.password, 'test password', 'Created user password different from expected')

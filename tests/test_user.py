import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
    """This checks that every behaviour of the User model class is true

    Args:
        unittest.TestCase ([unittest]): [This is the model where we get most of the test functionality from]
    """
    def setUp(self):
        """This runs before every test does
        """
        self.new_user = User(password = 'banana')

    def test_password_setter(self):
        """This makes sure that the password created is not none
        """
        self.assertTrue(self.new_user.pass_secure is not None)
from unittest import TestCase
from app.config import TestConfig
from app import create_app, db
from app.controllers import sign_user_up, SignUpError, log_user_in, LoginError
from app.test_data import add_test_users_to_db
from app.models import User

class BasicUnitTests(TestCase):

    def setup(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_users_to_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_sign_up(self):
        with self.assertRaisesRegex(SignUpError, "Passwords do not match"):
            sign_user_up("NotRight", "Password", "NotPassword", False)
        with self.assertRaisesRegex(SignUpError, "Password must have at least 8 characters"):
            sign_user_up("NotRight", "P2a", "P2a", False)
        with self.assertRaisesRegex(SignUpError, "Password must have at least one upper case character"):
            sign_user_up("NotRight", "thisis8long", "thisis8long", False)
        with self.assertRaisesRegex(SignUpError, "Password must have at least one number"):
            sign_user_up("NotRight", "AAAAAaaaaaassss", "AAAAAaaaaaassss", False)
        with self.assertRaisesRegex(SignUpError, "User exists"):
            sign_user_up("Sibi", "AAAAAaaaaa3assss", "AAAAAa3aaaaassss", False)

    def test_log_in(self):

        with self.assertRaisesRegex(LoginError, "Please check your login details"):
            log_user_in("Alex", "SafePassword123", False)
        with self.assertRaisesRegex(LoginError, "Please check your login details"):
            log_user_in("Sibi", "SafePassword123", False)
        with self.assertRaisesRegex(LoginError, "Please check your login details"):
            log_user_in("Daniel", "SafePassword123", False)
        with self.assertRaisesRegex(LoginError, "Please check your login details"):
            log_user_in("Cooper", "SafePassword123", False)
from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):
    def test_str_returns_username(self):
        user = CustomUser.objects.create(username="testuser")
        self.assertEqual(str(user), "testuser")

# Add more tests for validation and custom fields as needed

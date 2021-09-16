from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
from django.conf import settings


class DjangoConfigTest(TestCase):
 #https://docs.python.org/3/library/unittest.html
 #https://www.youtube.com/watch?v=6I_haJimhPY&t=28s
    def test_secret_key_strength(self):
      SECRET_KEY = settings.SECRET_KEY
      #self.assertNotEqual(SECRET_KEY, 'abc')
      
      try:
         is_strong = validate_password(SECRET_KEY)
      except Exception as e:
         msg = f'Weak secret key {e.messages}'
         self.fail(msg)
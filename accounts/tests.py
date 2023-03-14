from django.test import TestCase

# Create your tests here.
import secrets
print(type(secrets.randbelow(10**8)))
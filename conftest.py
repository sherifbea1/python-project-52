import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))

def pytest_configure():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hexlet_code.settings'
    django.setup()
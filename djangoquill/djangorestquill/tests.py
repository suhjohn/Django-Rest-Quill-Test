from django.test import TestCase

# Create your tests here.


# Test for Problems such as
# What if content doesn't exist?
# What if content is in wrong format?
# What if content length is 0?
# What if content length is super long?

# What happens when we update?
from rest_framework.test import APITestCase


class QuillRelatedModelCreateTest(APITestCase):

    def test_quillpost_related_model_create(self):
        url = "/answer/"


from django.test import TestCase

# Create your tests here.
class TestCalls(TestCase):

    def test_call_view_loads(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg='View is not reachable')

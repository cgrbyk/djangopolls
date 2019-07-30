from django.test import TestCase

# Create your tests here.
class TestCalls(TestCase):
    def test_call_view_loads(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200, msg="View is not reachable")
        self.assertTemplateUsed(response, 'index.html')

    def test_log_in(self):
        resp = self.client.post("/login", {"username": 1})
        print(resp)
        self.assertEqual(resp.status_code, 200)

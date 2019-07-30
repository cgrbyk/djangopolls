from django.test import TestCase

# Create your tests here.
class TestCalls(TestCase):

    def test_call_view_loads(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg='View is not reachable')
    
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        

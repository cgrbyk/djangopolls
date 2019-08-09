import json
from django.contrib.auth.models import User
from polls.models import Question, Choice
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.utils import timezone

# Create your tests here.
# http http://127.0.0.1:8000/hello/ 'Authorization: Token 7f423d527b6937eae72a54fde82e5f914ad31db5'
# http post http://127.0.0.1:8000/api-token-auth/ username=cgrbyk password=123


class CoreTests(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.get_token()
        self.api_authentication()
        q1 = Question.objects.create(
             question_text="soru 1", pub_date=timezone.now()
        )
        self.q1_id = q1.id
        q2 = Question.objects.create(
             question_text="soru 2", pub_date=timezone.now()
        )
        self.q2_id = q2.id
        c1 = Choice.objects.create(
            question=q1, choice_text="secenek 1", votes=0
        )
        self.c1_id = c1.id
        Choice.objects.create(
            question=q1, choice_text="secenek 2", votes=0
        )
        Choice.objects.create(
            question=q1, choice_text="secenek 3", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="secenek 1", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="secenek 2", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="secenek 3", votes=0
        )
        # self.Question_Choice_list()

    def get_token(self):
        response = self.client.post('/api/token/', data={'username': self.username, 'password': self.password})
        tokens = json.loads(response.content)
        print(tokens)
        self.token = tokens['access']

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_login_success(self):
        response = self.client.login(username=self.username, password=self.password)
        self.assertEqual(response, True)

    def test_login_fail(self):
        response = self.client.login(username='wronguser', password='wrongpassword')
        self.assertEqual(response, False)

    def test_hello_get(self):
        response = self.client.get('/hello/')
        print(json.loads(response.content))
        self.assertEqual(json.loads(response.content)['message'], 'Hello, World !!')

    # response should return question list
    def test_api_question_get(self):
        response = self.client.get('/question/')
        data = json.loads(response.content)
        self.assertEqual(data[0]['id'], Question.objects.all().first().id)
        self.assertEqual(data[0]['question_text'], Question.objects.all().first().question_text)

    # response should return choice list
    def test_api_choice_get(self):
        response = self.client.get('/choice/')
        data = json.loads(response.content)
        print(data)
        cho = Choice.objects.all().first()
        que = Question.objects.all().first()
        self.assertEqual(data[0][str(que.id)], que.question_text)
        self.assertEqual(data[0][str(que.id)+'-'+str(cho.id)], cho.choice_text)

    # vote api should increment choice's votes
    def test_api_vote(self):
        choice_cote_count_before_post = Choice.objects.filter(id=self.c1_id).first().votes
        response = self.client.post('/vote/', data={'c_id': self.c1_id})
        choice_cote_count_after_post = Choice.objects.get(id=self.c1_id).votes
        self.assertEqual(choice_cote_count_before_post+1, choice_cote_count_after_post)

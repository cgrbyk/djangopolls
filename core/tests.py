import json
from django.contrib.auth.models import User
from polls.models import Question, Choice
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Create your tests here.
# http http://127.0.0.1:8000/hello/ 'Authorization: Token 7f423d527b6937eae72a54fde82e5f914ad31db5'
# http post http://127.0.0.1:8000/api-token-auth/ username=cgrbyk password=123


class CoreTests(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        Question.objects.create(
            question_text="soru 1", pub_date=datetime.datetime.now()
        )
        Question.objects.create(
            question_text="soru 2", pub_date=datetime.datetime.now()
        )
        Choice.objects.create(
            question=Question.objects.get(id=1), choice_text="secenek 1", votes=0
        )
        Choice.objects.create(
            question=Question.objects.get(id=1), choice_text="secenek 2", votes=0
        )
        Choice.objects.create(
            question=Question.objects.get(id=1), choice_text="secenek 3", votes=0
        )
        Choice.objects.create(
            question=Question.objects.get(id=2), choice_text="secenek 1", votes=0
        )
        Choice.objects.create(
            question=Question.objects.get(id=2), choice_text="secenek 2", votes=0
        )
        Choice.objects.create(
            question=Question.objects.get(id=2), choice_text="secenek 3", votes=0
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

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

    # dönen token ile hafızadaki token aynı olup olmaması kontrol ediliyor.
    def test_token_get(self):
        response = self.client.post('/api-token-auth/', data={'username': self.username, 'password': self.password})
        # print(json.loads(response.content)['token'])
        self.assertEqual(json.loads(response.content)['token'], self.token.key)

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
        choice_cote_count_before_post = Choice.objects.get(id=1).votes
        response = self.client.post('/vote/', data={'c_id': 1})
        choice_cote_count_after_post = Choice.objects.get(id=1).votes
        self.assertEqual(choice_cote_count_before_post+1, choice_cote_count_after_post)



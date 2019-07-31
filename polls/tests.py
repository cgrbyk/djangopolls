from django.test import TestCase
import datetime

from polls import models

class PollTestCase(TestCase):

    def setUp(self):
        Question.objects.create(question_text="soru 1", pub_date=datetime.datetime.now())
        Question.objects.create(question_text="soru 2", pub_date=datetime.datetime.now())
        Choice.objects.create(Question.objects.get(id=1),choice_text="şık 1", votes=0)
        Choice.objects.create(Question.objects.get(id=1),choice_text="şık 2", votes=0)
        Choice.objects.create(Question.objects.get(id=1),choice_text="şık 3", votes=0)
        Choice.objects.create(Question.objects.get(id=2),choice_text="şık 1", votes=0)
        Choice.objects.create(Question.objects.get(id=2),choice_text="şık 2", votes=0)
        Choice.objects.create(Question.objects.get(id=2),choice_text="şık 3", votes=0)

    def test_question_count(self):
        questions = Question.objects.all()
        self.assertEqual(questions.count,2)
    
    def test_choice_count(self):
        choices = Choice.objects.filter(question.id=1)
        self.assertEqual(Choices.count,3)
        choices = Choice.objects.filter(question.id=2)
        self.assertEqual(Choices.count,3)
    
    def test_question_get(self):
        que=Question.objects.get(id=1)
        self.assertNotEqual(que,None)
    
    def  test_fail_get(self):
        que=Question.objects.get(id=15749214)
        self.assertEqual(que,None)

    def test_vote(self):
        choices=Choices.objects.filter(question.id=1)
        for cho in choices:
            self.assertAlmostEqual(cho.votes,0)
        choices[2].vote=choices[2].vote + 1
        self.assertEqual(choices[2].vote, 1)

    def test_load_succes(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg= 'View is not reachable')
        self.assertTemplateUsed(response, 'index.html')
        response = self.client.get('questionlist')
        self.assertEqual(response.status_code, 200, msg= 'View is not reachable')
        self.assertTemplateUsed(response, 'questionlist.html')
        response = self.client.get('vote/1')
        self.assertEqual(response.status_code, 200, msg= 'View is not reachable')
        self.assertTemplateUsed(response, 'vote.html')
    
    def test_load_fail(self):
        response = self.client.get('vote/14352345')
        self.assertEqual(response.status_code, 404, msg= 'Should be 404')
        self.assertTemplateUsed(response, 'vote.html')
    
    def test_vote_inc(self):
        cho_first_vote_count = Choices.objects.get(id=1).vote
        esponse = self.client.get('vote/1')
        self.assertEqual(response.status_code, 200)
        cho_second_vote_count = Choices.objects.get(id=1).vote
        self.assertEqual(cho_first_vote_count+1,cho_second_vote_count)
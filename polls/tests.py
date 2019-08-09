from django.test import TestCase
from django.utils import timezone
from .models import Question, Choice


class PollTestCase(TestCase):
    def setUp(self):
        q1 = Question.objects.create(
            question_text="soru 1", pub_date=timezone.now()
        )
        self.q1_id = q1.id
        q2 = Question.objects.create(
            question_text="soru 2", pub_date=timezone.now()
        )
        self.q2_id = q2.id
        c1 = Choice.objects.create(
            question=q1, choice_text="şık 1", votes=0
        )
        self.c1_id = c1.id
        Choice.objects.create(
            question=q1, choice_text="şık 2", votes=0
        )
        Choice.objects.create(
            question=q1, choice_text="şık 3", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="şık 1", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="şık 2", votes=0
        )
        Choice.objects.create(
            question=q2, choice_text="şık 3", votes=0
        )

    def test_question_count(self):
        questions = Question.objects.all()
        self.assertEqual(questions.count(), 2)

    def test_choice_count(self):
        que = Question.objects.get(id=self.q1_id)
        choices = Choice.objects.filter(question=que)
        self.assertEqual(choices.count(), 3)
        que = Question.objects.get(id=self.q2_id)
        choices = Choice.objects.filter(question=que)
        self.assertEqual(choices.count(), 3)

    def test_question_get(self):
        que = Question.objects.get(id=self.q1_id)
        self.assertNotEqual(que, None)

    def test_fail_get(self):
        que = Question.objects.filter(id=15749214)
        self.assertEqual(que.count(), 0)

    def test_vote(self):
        que = Question.objects.get(id=self.q1_id)
        choices = Choice.objects.filter(question=que)
        for cho in choices:
            self.assertAlmostEqual(cho.votes, 0)
        choices[2].votes = choices[2].votes + 1
        self.assertEqual(choices[2].votes, 1)

    def test_load_succes(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg="View is not reachable")
        self.assertTemplateUsed(response, "questionlist.html")
        response = self.client.get("/vote/"+str(self.q1_id))
        self.assertEqual(response.status_code, 200, msg="View is not reachable")
        self.assertTemplateUsed(response, "vote.html")

    def test_load_fail(self):
        response = self.client.get("/vote/14352345")
        self.assertEqual(response.status_code, 404, msg="Should be 404")

    def test_vote_inc(self):
        cho_first_vote_count = Choice.objects.get(id=self.c1_id).votes
        response = self.client.post('/vote/incvote', {'cid': self.c1_id})
        self.assertEqual(response.status_code, 302)
        cho_second_vote_count = Choice.objects.get(id=self.c1_id).votes
        self.assertEqual(cho_first_vote_count + 1, cho_second_vote_count)

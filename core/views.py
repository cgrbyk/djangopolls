from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
from polls import models
from django.core import serializers
import datetime


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World !!'}
        return Response(content)

    def post(self, request):
        print(request)
        return Response('sdfg')


class QuestionAPI(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        questions = models.Question.objects.all().values()
        question_list = list(questions)
        return JsonResponse(question_list, safe=False)

    def post(self, request):
        question_text = request.POST.get('question_text')
        pub_date = datetime.datetime.now()
        q = models.Question.objects.create(question_text=question_text, pub_date=pub_date)
        return Response(q.id)


class ChoiceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = dict()
        response_list = []
        for que in models.Question.objects.all():
            content[str(que.id)] = que.question_text
            for cho in models.Choice.objects.filter(question_id=que.id):
                content[str(que.id)+'-'+str(cho.id)] = cho.choice_text
            response_list.append(content)
            content = dict()
        return JsonResponse(response_list, safe=False)

    def post(self, request):
        choice_text = request.POST.get('choice_text')
        q_id = request.POST.get('q_id')
        c = models.Choice.objects.create(question=models.Question.objects.get(id=q_id), choice_text=choice_text, votes=0)
        return Response(c.id)


class VoteAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        c_id = request.POST.get('c_id')
        choice = models.Choice.objects.get(id=c_id)
        choice.votes = choice.votes+1
        choice.save()
        return HttpResponse('Voted')


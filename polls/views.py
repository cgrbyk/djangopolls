from django.shortcuts import render, HttpResponse, redirect
from .models import Question, Choice
from django.contrib.auth.models import User, auth

# Create your views here.


def index(request):
    return render(request, "index.html", {})


def questionlist(request):
    if request.method == "GET":
        return redirect("/")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            ques = Question.objects.all()
            return render(request, "questionlist.html", {"ques": ques})
        else:
            return redirect('/')


def questions(request, qid):
    ques = Question.objects.filter(id=qid)
    cho = Choice.objects.filter(question=ques[0])
    return render(request, "question.html", {"choices": cho})

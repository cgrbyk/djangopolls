from django.shortcuts import render
from .models import Question,Choice

# Create your views here.

def questionlist(request):
    questions = Question.objects.all()
    return render(request,'questionlist.html',{'questions':questions})
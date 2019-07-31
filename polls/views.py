from django.shortcuts import render,redirect,get_object_or_404
from .models import Question,Choice

# Create your views here.

def questionlist(request):
    questions = Question.objects.all()
    return render(request,'questionlist.html',{'questions':questions})

def vote(request,id):
    question_to_list = get_object_or_404(Question, id = id)
    choices = Choice.objects.filter(question = question_to_list)
    return render(request,'vote.html',{'choices':choices})

def incvote(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        cho = Choice.objects.get(id = cid)
        cho.votes=cho.votes+1
        cho.save()
        return redirect('/')
    else:
        return redirect('/')
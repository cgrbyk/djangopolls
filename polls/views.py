from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

def index(request):
    return render(request,'index.html',{})

def login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        return HttpResponse(username+' '+password)

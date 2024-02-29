from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Receipe
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def Home (request):
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    context = {'receipes': queryset}
    return render(request ,"home.html", context)

@login_required(login_url='/login/')
def receipe(request):
    if(request.method == "POST"):
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get("receipe_image")

        Receipe.objects.create(
            receipe_name= receipe_name,
            receipe_description= receipe_description,
            receipe_image= receipe_image,        
        )
        return redirect("/")
    
    return render(request, "receipe.html",)
    
@login_required(login_url='/login/')
def delete(request, id):
    queryset = Receipe.objects.get(id = id)
    # print(queryset.receipe_image)
    queryset.receipe_image.delete()
    queryset.delete()
    return redirect("/")

@login_required(login_url='/login/')
def update(request, id):
    queryset = Receipe.objects.get(id = id)
    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")
        receipe_image = request.FILES.get("receipe_image")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()
        return redirect("/")
    contex = { 'receipe' : queryset}
    return render(request, 'update.html', contex)


def about(request):
    return render(request , 'about.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user  = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username is already taken.")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.error(request, "Successfull Registration.")
        return redirect('/login/')

    return render(request, 'register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Username is not exist.")
            return render(request, 'login.html')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Password did not match")
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')
        

def logout_page(request):
    logout(request)
    return redirect('/login/')

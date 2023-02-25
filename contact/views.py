from django.shortcuts import render,redirect,Http404 
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .forms import  ContactBookForm
from .models import ContactBook
from django.contrib import messages

# Create your views here.

def logout_reguest(requeest):
    if requeest.user.is_authenticated():
        logout(requeest )
        return redirect("index")
    else:
        return Http404()
def index(request):
    allcontact=ContactBook.objects.filter(user=request.user).order_by("-created")
    return render(request,"index.html",context={"allcontact":allcontact})

def LoginView(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method=="POST":#post eildimi diye bakıyor 
        username=request.POST["username"]# bilgileri alıyorum 
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)#burada kişi varmı diye bakıyorum 
        if user is not None:
            login(request,user)
            return redirect("index")
        else :
            return render (request,"login.html",{
                "error":"username yada parola yanlış"
            })
    return render(request,"login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        repassword=request.POST["repassword"]
        if password==repassword:
            if User.objects.filter(username=username).exists():
                return render(request,"register.html",{
                "error":"kullanıcı mevcut",
                })
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                messages.success(request,"basarılı bir şekilde olusturdunuz")

                return redirect("login")
        else:
            return render(request,"register.html",{"error":"şifreler aynı değil"})
    return render(request,"register.html")

def create(request):# burada farklı bir metot yapılıyor djangonun sablonlarını kullaıyoruz
    if request.user.is_authenticated:#buradamısafır kullanıcılar arama cubuguna bile yazsa buraya bakmasını engelliyorum 
        contactBookForm=ContactBookForm()
        if request.method=="POST":
            contactBookForm = ContactBookForm(request.POST or None,request.FILES or None)
        if contactBookForm.is_valid():
            contactBookForm=contactBookForm.save(commit=False)
            contactBookForm.user=request.user
            contactBookForm.save()
            messages.success(request,"basarılı bir şekilde olusturdunuz")

            return redirect("index")
        else:
            print (contactBookForm.errors)

        return render(request,"create.html",context={"contactBookForm":contactBookForm})
   

    else:
        return Http404()


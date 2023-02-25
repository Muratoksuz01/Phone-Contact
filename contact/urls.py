from django.urls import path
from .views import *


urlpatterns=[

    path("",index,name="index"),
    path("login/",LoginView,name="login"),
    path("register/",register,name="register"),
    path("logout/",logout_reguest,name="logout"),
    path("create/",create,name="create"),



]
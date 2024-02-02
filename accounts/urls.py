from django.urls import include , path 

from rest_framework.routers import DefaultRouter
from accounts import views

#using ObtainAuthToken class to generate authentication toekns
from rest_framework.authtoken.views import ObtainAuthToken

#setting up routers to link up UserViews
router = DefaultRouter()
router.register(r'users' , views.UserViewAPI)

urlpatterns = [
    path('' , include(router.urls)),
    path('register/' , views.UserRegisterAPI.as_view()),
    path('login/' , ObtainAuthToken.as_view()),
    path('logout/' , views.LogoutAPI),
]

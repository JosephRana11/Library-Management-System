from django.urls import include , path 

from rest_framework.routers import DefaultRouter
from accounts import views

#setting up routers to link up UserViews
router = DefaultRouter()
router.register(r'users' , views.UserViewAPI)

urlpatterns = [
    path('' , include(router.urls)),
    path('register' , views.UserRegisterAPI.as_view())
]

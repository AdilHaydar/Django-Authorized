from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name = "login"),
    path('register/',views.register,name = "register"),
    path('logout/',views.logoutUser,name = "logout"),
    path('edit/<str:username>',views.change_user,name="user-edit"),
    path('view/<str:username>',views.view_user,name="user-view"),
]
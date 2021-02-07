from django.urls import path
from . import views
urlpatterns = [
    path('', views.view_post,name = "view_post"),
    path('blog/add',views.add_post,name="add_post"),
    path('blog/show-<int:pk>',views.show_post,name="show_post"),
    path('blog/edit_post-<int:pk>',views.edit_post,name="edit_post"),

]
from blog import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='blog_view'),
    path('blogpost<int:myid>', views.blogpost, name='blog_post'),
]

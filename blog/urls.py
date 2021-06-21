from blog import views
from django.urls import path

urlpatterns = [
    path('', views.blog_view, name='blog_view')
]

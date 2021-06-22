from django.shortcuts import render
from .models import Blogpost
from django.http import HttpResponse
# Create your views here.
def index(request):
    myposts= Blogpost.objects.all()
    print(myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})
def blogpost(request, myid):
    post = Blogpost.objects.filter(post_id = myid)[0]
    print(post)
    return render(request, 'blog/post.html',{'post':post})

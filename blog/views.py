from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def blog_view(request):
    return render(request, 'blog/index.html')

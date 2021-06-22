from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('about/', views.shop_about, name='aboutUs'),
    path('contact/', views.shop_contact, name='contactUs'),
    path('tracker/', views.shop_tracker, name='TrackingOrder'),
     path("products<int:myid>", views.productView, name="ProductView"),
    path('checkout/', views.shop_checkout, name='CheckOut'),
    path('login/', views.shop_login, name='Login'),
    path('signup/', views.shop_signup, name='SignUp'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('search/', views.search, name='search')
]

from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view),  # Si la función se llama hello_view
  
]

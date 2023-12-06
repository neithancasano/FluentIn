from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('get_new_word', views.get_new_word, name='get_new_word'), # we get a new word from gpt 4.0
]
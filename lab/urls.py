from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classroom/<str:pk>', views.classroom, name='classroom'),
    path('create_class/', views.create_class, name='create_class'),
    path('create_assignment/<str:pk>', views.create_assignment, name='create_assignment'),
    path('question/<str:pk>', views.question, name='question'),
    path('add_answer/<str:pk>', views.add_answer, name='add_answer'),
    path('add_participants/<str:pk>', views.add_participants, name='add_participants'),
    path('create_poll/<str:pk>', views.create_poll, name='create_poll'),
]
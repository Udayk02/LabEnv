from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classroom/<str:pk>', views.classroom, name='classroom'),
    path('create_class/', views.create_class, name='create_class'),
    path('create_assignment/<str:pk>', views.create_assignment, name='create_assignment'),
    path('question/<str:pk>', views.question, name='question'),
    path('vote/<str:pk>', views.vote, name='vote'),
    path('add_answer/<str:pk>', views.add_answer, name='add_answer'),
    path('add_participants/<str:pk>', views.add_participants, name='add_participants'),
    path('create_poll/<str:pk>', views.create_poll, name='create_poll'),
    path('compiler_submit/<str:pk>/(?P<id>\d+)/$', views.submit_code, name='compiler_submit'),
    path('compiler_run/<str:pk>', views.run_code, name='compiler_run'),
    path('delete_assignment/<str:pk>', views.delete_assignment, name='delete_assignment'),
    path('delete_class/<str:pk>', views.delete_class, name='delete_class'),
]
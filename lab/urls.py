from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('classroom/<str:pk>', views.classroom, name='classroom'),
    path('create_class/', views.create_class, name='create_class'),
    path('create_assignment/<str:pk>', views.create_assignment, name='create_assignment'),
]
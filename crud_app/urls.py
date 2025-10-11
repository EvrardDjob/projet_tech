from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insert/', views.insert_student, name='insert_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('confirmation-suppression/<int:id>/', views.confirmation_suppression, name='confirmation_suppression'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
]
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:id>', views.view_student, name='view_student'),
  path('add/', views.add, name='add'),
  path('edit/<int:id>/', views.edit, name='edit'),
  path('delete/<int:id>/', views.delete, name='delete'),
  path('student/login/', views.student_login, name='student_login'),
  path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
  path('student/logout/', views.student_logout, name='student_logout'),
]
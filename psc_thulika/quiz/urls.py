from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Enter name before starting quiz
    path('quiz/<int:quiz_id>/name/', views.enter_name, name='enter_name'),

    # Quiz page
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz'),

    # Result page
    path('result/<int:quiz_id>/', views.result_view, name='result'),

    # Leaderboard
    path('leaderboard/<int:quiz_id>/', views.leaderboard, name='leaderboard'),

    # Admin panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/create-quiz/', views.create_quiz, name='create_quiz'),
    path('admin-panel/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    ]
from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_viwe, name='about'),
    path('contact/', views.contact_viwe, name='contact'),
    path('home/', views.HomePageView.as_view()),
    path('add/question/', views.QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:pk>/choises/', views.add_choises_to_question, name='question-choises'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/<int:pk>/vote/', views.ChoiseSelectView.as_view(), name='question-vote'),
    path('question/<int:pk>/results/', views.question_results_view, name='question-results'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question-edit'),
]

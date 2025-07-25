from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('process/<int:video_id>/', views.process_video, name='process_video'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]
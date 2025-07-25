from django.contrib import admin
from .models import Video, Quiz, Question

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'processed']
    list_filter = ['processed', 'uploaded_at']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'video', 'created_at']
    list_filter = ['created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_type', 'question_text']
    list_filter = ['question_type']
from django.db import models
import json

class Video(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    transcript = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('mc', 'Multiple Choice'),
        ('tf', 'True/False'),
        ('sa', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    options = models.JSONField(default=dict, blank=True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quiz.title} - Q{self.id}"
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Video, Quiz, Question
from .forms import VideoUploadForm
from .services import VideoProcessor
import json

def home(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'home.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    quizzes = Quiz.objects.filter(video=video)
    return render(request, 'video_detail.html', {
        'video': video,
        'quizzes': quizzes
    })

def process_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        try:
            processor = VideoProcessor()
            quiz = processor.process_video(video)

            return JsonResponse({
                'success': True,
                'quiz_id': quiz.id,
                'message': 'Quiz generated successfully!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error processing video: {str(e)}'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_detail.html', {
        'quiz': quiz,
        'questions': questions
    })
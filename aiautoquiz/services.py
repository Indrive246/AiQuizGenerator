import openai
import pathlib
from openai import OpenAI
import json
from django.conf import settings
from .models import Quiz, Question


class VideoProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def process_video(self, video):  
        transcript = self.transcribe_video(video)
        video.transcript = transcript
        video.processed = True
        video.save()
        quiz = self.generate_quiz(video, transcript)
        return quiz

    def transcribe_video(self, video):
        try:
            file_path = pathlib.Path(video.file.path)

            with file_path.open("rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript

        except Exception as e:
            raise Exception("Transcription failed. Please check the video/audio file.")
    def generate_quiz(self, video, transcript):
        prompt = f"""
    You are a helpful assistant. Create a quiz based on this transcript of a lecture.

    Transcript:
    {transcript[:3000]}

    Your task:
    - Generate a short quiz (around 5 questions).
    - Use ONLY multiple choice questions.
    - Make sure the quiz tests key concepts.
    - Format the output as JSON in this structure:

    {{
        "quiz_title": "A descriptive title",
        "questions": [
            {{
                "question_text": "What is X?",
                "question_type": "mc",
                "options": {{
                    "A": "Option 1",
                    "B": "Option 2",
                    "C": "Option 3",
                    "D": "Option 4"
                }},
                "correct_answer": "A",
                "explanation": "Explanation of the correct answer"
            }}
        ]
    }}
    """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educational assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            raw_response = response.choices[0].message.content

            quiz_data = json.loads(raw_response)
            return self.create_quiz_from_data(video, quiz_data)

        except Exception as e:
            raise Exception("Quiz generation failed. GPT-4 could not process the transcript.")


    def create_quiz_from_data(self, video, quiz_data):
        quiz = Quiz.objects.create(
            video=video,
            title=quiz_data.get('quiz_title', f'Quiz for {video.title}')
        )

        for q in quiz_data.get('questions', []):
            Question.objects.create(
                quiz=quiz,
                question_text=q['question_text'],
                question_type=q['question_type'],
                options=q.get('options', {}),
                correct_answer=q['correct_answer'],
                explanation=q.get('explanation', '')
            )
        return quiz

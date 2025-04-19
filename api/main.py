import os
import sys
import django
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Set up Django integration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stackoverflow_clone.settings')
django.setup()

from qna.models import Question
from django.core.exceptions import ObjectDoesNotExist

app = FastAPI(title="Stack Overflow Clone API")

class QuestionResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

@app.get("/")
async def root():
    return {"message": "Welcome to Stack Overflow Clone API"}

@app.get("/api/questions/", response_model=list[QuestionResponse])
async def get_questions():
    try:
        questions = Question.objects.all()
        return [
            QuestionResponse(
                id=q.id,
                title=q.title,
                content=q.content,
                author=q.author.username
            )
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int):
    try:
        q = Question.objects.get(id=question_id)
        return QuestionResponse(
            id=q.id,
            title=q.title,
            content=q.content,
            author=q.author.username
        )
    except ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail="Question not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
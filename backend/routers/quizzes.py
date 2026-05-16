from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(
    prefix="/api/quizzes",
    tags=["Quizzes"]
)

@router.get("/", response_model=List[schemas.QuizResponse])
def get_quizzes(db: Session = Depends(get_db)):
    return db.query(models.Quiz).all()

@router.get("/{quiz_id}", response_model=schemas.QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/", response_model=schemas.QuizResponse)
def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(['admin', 'faculty']))
):
    # Verify subject exists
    subject = db.query(models.Subject).filter(models.Subject.id == quiz.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    new_quiz = models.Quiz(
        title=quiz.title,
        description=quiz.description,
        duration_minutes=quiz.duration_minutes,
        total_marks=quiz.total_marks,
        subject_id=quiz.subject_id,
        created_by_id=current_user.id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

@router.post("/{quiz_id}/questions", response_model=schemas.QuestionResponse)
def add_question(
    quiz_id: int,
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(['admin', 'faculty']))
):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # In a real app, verify if the current user owns the quiz or is admin
    new_question = models.Question(
        quiz_id=quiz_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_option=question.correct_option,
        marks=question.marks
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

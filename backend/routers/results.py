from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(
    prefix="/api/results",
    tags=["Results"]
)

@router.get("/", response_model=List[schemas.ResultResponse])
def get_results(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role == 'student':
        return db.query(models.Result).filter(models.Result.student_id == current_user.id).all()
    else:
        # Faculty or Admin can see all results
        return db.query(models.Result).all()

@router.post("/submit", response_model=schemas.ResultResponse)
def submit_quiz(
    submission: schemas.QuizSubmission,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(['student']))
):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    score = 0
    # Evaluate answers
    for answer_sub in submission.answers:
        question = db.query(models.Question).filter(
            models.Question.id == answer_sub.question_id,
            models.Question.quiz_id == quiz.id
        ).first()
        if question and question.correct_option == answer_sub.selected_option:
            score += question.marks
            
    percentage = (score / quiz.total_marks) * 100 if quiz.total_marks > 0 else 0

    result = models.Result(
        student_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        total_marks=quiz.total_marks,
        percentage=percentage
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

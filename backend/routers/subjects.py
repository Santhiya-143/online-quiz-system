from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas, auth

router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"]
)

@router.get("/", response_model=List[schemas.SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()

@router.post("/", response_model=schemas.SubjectResponse)
def create_subject(
    subject: schemas.SubjectCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(['admin', 'faculty']))
):
    db_subject = db.query(models.Subject).filter(models.Subject.code == subject.code).first()
    if db_subject:
        raise HTTPException(status_code=400, detail="Subject code already exists")
    
    new_subject = models.Subject(
        name=subject.name,
        code=subject.code,
        description=subject.description,
        created_by_id=current_user.id
    )
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

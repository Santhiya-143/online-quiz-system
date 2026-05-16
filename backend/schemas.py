from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Subject Schemas
class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    created_by_id: int
    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    marks: int

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int
    class Config:
        from_attributes = True

# Quiz Schemas
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    total_marks: int
    subject_id: int

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: int
    created_by_id: int
    questions: List[QuestionResponse] = []
    class Config:
        from_attributes = True

# Result Schemas
class ResultBase(BaseModel):
    quiz_id: int
    score: int
    total_marks: int

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: int
    student_id: int
    percentage: float
    submitted_at: datetime
    class Config:
        from_attributes = True

# Answer Submission Schema
class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str

class QuizSubmission(BaseModel):
    quiz_id: int
    answers: List[AnswerSubmission]

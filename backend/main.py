from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, subjects, quizzes, results

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Quiz System API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(quizzes.router)
app.include_router(results.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Quiz System API"}

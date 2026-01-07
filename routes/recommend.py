from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import RecommendRequest
from database import SessionLocal
from models import StudentAIUsage, AIProjectRecommendation
from services.ai_gen import generate_project
from services.prompt_builder import build_prompt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recommend-project")
def recommend_project(
    data: RecommendRequest,
    db: Session = Depends(get_db)
):
    # 1️⃣ Get or create usage
    usage = db.query(StudentAIUsage)\
              .filter_by(student_id=data.student_id)\
              .first()

    if not usage:
        usage = StudentAIUsage(
            student_id=data.student_id,
            recommendation_count=0,
            locked=False
        )
        db.add(usage)
        db.commit()
        db.refresh(usage)

    # 2️⃣ Lock check
    if usage.recommendation_count >= 5:
        projects = db.query(AIProjectRecommendation)\
                     .filter_by(student_id=data.student_id)\
                     .all()

        return {
            "locked": True,
            "message": "Maximum AI recommendations reached",
            "projects": [p.project_payload for p in projects]
        }

    # 3️⃣ Build prompt
    previous = db.query(AIProjectRecommendation)\
                 .filter_by(student_id=data.student_id)\
                 .all()

    previous_titles = [p.project_title for p in previous]

    prompt = build_prompt(
        student=data.dict(),
        previous_titles=previous_titles
    )

    # 4️⃣ Generate AI project
    project_json = generate_project(prompt)

    attempt = usage.recommendation_count + 1

    # 5️⃣ Save project
    db.add(AIProjectRecommendation(
        student_id=data.student_id,
        attempt_no=attempt,
        project_title=project_json["title"],
        project_payload=project_json
    ))

    usage.recommendation_count = attempt
    if attempt == 5:
        usage.locked = True

    db.commit()

    return {
        "attempt": attempt,
        "project": project_json
    }

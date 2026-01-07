from sqlalchemy import Column, Integer, BigInteger, Boolean, String, JSON
from database import Base

class StudentAIUsage(Base):
    __tablename__ = "student_ai_usage"

    student_id = Column(BigInteger, primary_key=True, index=True)
    recommendation_count = Column(Integer, default=0)
    locked = Column(Boolean, default=False)


class AIProjectRecommendation(Base):
    __tablename__ = "ai_project_recommendations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    student_id = Column(BigInteger, index=True)
    attempt_no = Column(Integer)
    project_title = Column(String(255))
    project_payload = Column(JSON)

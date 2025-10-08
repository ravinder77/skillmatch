from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.candidate_profile import CandidateProfile


def get_profile_by_id(
        db: Session,
        user_id: int,
) -> CandidateProfile | None:

    result = db.execute(select(CandidateProfile).where(CandidateProfile.user_id == user_id ))
    return result.scalar_one_or_none()

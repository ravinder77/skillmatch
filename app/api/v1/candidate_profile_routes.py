from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from app.db.session import get_db
from app.models.candidate_profile import CandidateProfile
from app.models.user import User
from app.api.dependencies import get_current_user

from app.schemas.candidate_profile import CandidateProfileResponse, CandidateProfileCreate, CandidateProfileUpdate, \
    CandidateProfilePublicView
from app.utils.helpers import unique_slug_generator

router = APIRouter()


@router.post("/profile", response_model=CandidateProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(profile_in: CandidateProfileCreate,
                         db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[User, Depends(get_current_user)],
):

    if current_user.role.value != "candidate":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to perform this action."
    )

    slug = unique_slug_generator(current_user.first_name, separator='-')

    profile = CandidateProfile(
        user_id=current_user.id,
        profile_image_url= str(profile_in.profile_image_url),
        headline=profile_in.headline,
        summary=profile_in.summary,
        location=profile_in.location,
        education=profile_in.education,
        github_url=str(profile_in.github_url) if profile_in.github_url else None,
        linkedin_url=str(profile_in.linkedin_url) if profile_in.linkedin_url else None,
        slug=slug,
        is_public=profile_in.is_public,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/profile/me", response_model=CandidateProfileResponse, status_code=status.HTTP_200_OK)
async def get_profile(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.put("/profile/update", response_model=CandidateProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(
        profile_in: CandidateProfileUpdate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)]
):

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    for field, value in profile_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


 # =============Public/Employer View ==============


@router.get("/profile/{slug}", response_model=CandidateProfilePublicView, status_code=status.HTTP_200_OK)
async def view_candidate_profile(
        slug: str,
        db: Annotated[Session, Depends(get_db)],
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.slug == slug).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    if not profile.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidate is not public."
        )

    return CandidateProfilePublicView.model_validate(profile)
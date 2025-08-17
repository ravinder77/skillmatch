
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.models import Skill
from app.schemas.skill import SkillResponse, SkillCreate, SkillUpdate

router = APIRouter()



@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """
    Create a new skill
    """
    existing_skill = db.query(Skill).filter(Skill.name == skill.name).first()
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists",
        )
    new_skill = Skill(name=skill.name, description=skill.description)

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get("/", response_model=List[SkillResponse], status_code=status.HTTP_200_OK)
async def read_skills(db: Session = Depends(get_db)):
    """
    List all skills
    """
    return db.query(Skill).all()


@router.get("/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_200_OK)
async def read_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    return skill


@router.put("/{skill_id}", response_model=SkillResponse, status_code=status.HTTP_200_OK)
async def update_skill(skill_id: int, skill_data: SkillUpdate, db: Session = Depends(get_db)):

    # check if skill is there
    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    # data to be updated
    update_data = skill_data.model_dump(exclude_unset=True)

    db.query(Skill).filter(Skill.id == skill_id).update(update_data)

    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: int, db: Session = Depends(get_db)):

    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )

    db.delete(skill)
    db.commit()

    return None
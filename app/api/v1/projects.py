from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List, Annotated

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Project, User, Skill
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from ..dependencies import get_current_user

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
        project_data: ProjectCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
     ):
    """  Create a new project and assign skills """

    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        status=project_data.status,
        github_url=str(project_data.github_url) if project_data.github_url else None,
        demo_url=str(project_data.demo_url) if project_data.demo_url else None,
        image_url=str(project_data.image_url) if project_data.image_url else None,
        user_id=current_user.id,
    )

    #
    if project_data.skills_id:
        # find all the skills whose id matches with the one of the ids user provided
        skills = db.query(Skill).filter(Skill.id.in_(project_data.skills_id)).all()
        new_project.skills.extend(skills)


    # commit to the db
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project




@router.get("/projects", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
async def get_projects(

        db: Session = Depends(get_db)):
    pass


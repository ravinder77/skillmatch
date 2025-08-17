from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from ..dependencies import get_current_user

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
        project_data: ProjectCreate,
        db: Session = Depends(get_db),
        current_user = Depends()


     ):
    """
    Create a new project and assign skills
    """


@router.get("/projects", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
async def get_projects(db: Session = Depends(get_db)):


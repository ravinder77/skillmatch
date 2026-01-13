from sqlmodel import SQLModel

# Import ALL models here
from app.models.user import User

# Expose metadata
metadata = SQLModel.metadata


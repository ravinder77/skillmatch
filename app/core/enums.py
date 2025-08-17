import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    EMPLOYER = "employer"


# Project Status Enum
class ProjectStatus(enum.Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    PLANNED = "Planned"

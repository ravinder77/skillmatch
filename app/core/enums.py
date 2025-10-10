from enum import Enum

class UserRole(str, Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ADMIN = "admin"

# Project Status Enum
class ProjectStatus(str, Enum):
    IN_PROGRESS = "in Progress"
    COMPLETED = "completed"
    PLANNED = "planned"


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

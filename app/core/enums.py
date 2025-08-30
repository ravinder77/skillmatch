import enum

class UserRole(enum.Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ADMIN = "admin"

# Project Status Enum
class ProjectStatus(enum.Enum):
    IN_PROGRESS = "in Progress"
    COMPLETED = "completed"
    PLANNED = "planned"

class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    SHORTLISTED = "reviewed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


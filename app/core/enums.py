import enum


class UserRole(enum.Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ADMIN = "admin"


# Project Status Enum
class ProjectStatus(enum.Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    PLANNED = "Planned"

class ApplicationStatus(enum.Enum):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"
    ACCEPTED = "Accepted"
    
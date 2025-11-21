from enum import Enum

class UserRole(str, Enum):
    APPLICANT = "applicant"
    EMPLOYER = "employer"
    ADMIN = "admin"

# Project Status Enum
class ProjectStatus(str, Enum):
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    PLANNED = "planned"

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class JobType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-Time"
    CONTRACT = "contract"

class JobStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"

class CompanySize(Enum):
    SMALL = "1-50"
    MEDIUM = "51-200"
    LARGE = "201-1000"
    ENTERPRISE = "1000+"
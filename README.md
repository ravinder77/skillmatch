
#APP ENDPOINTS

/api/v1/
├── auth/
│   ├── POST /signup
│   ├── POST /login
│   ├── POST /refresh
│   └── POST /logout
├── users/
│   ├── GET /me
│   ├── PUT /me
│   └── DELETE /me
├── skills/
│   ├── GET /
│   ├── POST /
│   ├── GET /{skill_id}
│   ├── PUT /{skill_id}
│   └── DELETE /{skill_id}
├── projects/
│   ├── GET /
│   ├── POST /
│   ├── GET /{project_id}
│   ├── PUT /{project_id}
│   └── DELETE /{project_id}
├── portfolio/
│   ├── GET /{username}
│   └── GET /{username}/stats
└── ai/
    ├── GET /suggestions
    ├── POST /analyze-github
    └── GET /skill-trends# skillmatch

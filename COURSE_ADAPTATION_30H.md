# GameHub Microservices Course — 30-Hour Adaptation

**Context**: Original curriculum designed for ~60–90 hours. This document requests a redesign for a **30-hour intensive** course at EPITA for CS students with Python and API experience.

---

## Current State

The full course spans **10 modules** across ~70 hours:

- **Modules 1–3** (10h): Local development, FastAPI, SQLite
- **Modules 4–10** (60h): Infrastructure (Docker, Kafka, RabbitMQ), observability, deployment

## Proposed Scope: Modules 1–3 Only

**Time budget**: 30 hours total
- Module 1: 3–4h (design thinking)
- Module 2: 8–10h (build services)
- Module 3: 6–8h (inter-service communication)
- Buffer: 4–6h (debugging, Q&A, office hours)

**Target outcome**: Students build a working 3-service distributed system locally, understand architectural patterns, and hit the limits of synchronous communication (motivating why Modules 4–10 exist).

---

## Specific Requests for Redesign

### 1. Module 1: Compress Design Thinking
**Current state**: Conceptual exercise on service decomposition, bounded contexts, CAP theorem.

**Requests**:
- Add a 15-minute **visual reference diagram** of the final GameHub architecture (ASCII art or simple SVG embed)
- Reduce discussion questions from 5 to **3 core questions** (remove CAP theorem depth for now)
- Add a **checklist format** so students can self-verify they've identified the right services
- Suggest: Include a pre-filled template with 2–3 bounded contexts already done as examples

**Why**: Students need quick orientation, not deep theory. They'll understand CAP when they *hit* it in Module 4.

---

### 2. Module 2: Provide Starter Templates

**Current state**: Students build `game-service` from scratch by following user-service pattern.

**Requests**:
- Create a **generator script or cookiecutter template** that scaffolds:
  - `services/{service-name}/` structure
  - `requirements.txt` with FastAPI, SQLAlchemy, pytest, alembic pre-pinned
  - `app/main.py` (empty FastAPI app skeleton)
  - `app/models.py` (empty SQLAlchemy base)
  - `app/schemas.py` (empty Pydantic schemas)
  - `app/repository.py` (empty async repository class)
  - `tests/test_health.py` (passing smoke test)
  - `.env` file template
  
- **Provide a worked example** for user-service with:
  - Clear docstrings on each layer
  - Comments marking DDD layers (domain/application/infrastructure)
  - One test example already written (e.g., `test_create_user`)

- **Add a "common mistakes" section**:
  - Async context manager misuse with httpx
  - SQLAlchemy session management
  - Circular imports in repository pattern

**Why**: Scaffolding saves 2–3 hours. Students focus on logic, not boilerplate.

---

### 3. Module 3: Simplify Inter-Service Communication

**Current state**: 
- Part A: REST + httpx + tenacity retry logic
- Part B: gRPC bonus (optional)

**Requests**:
- **Keep REST + httpx as core** (straightforward, students know HTTP)
- **Move gRPC to optional reading** (nice-to-know, not required for time budget)
- Add a **practical section on resilience patterns**:
  - Circuit breaker pattern (link to `pybreaker` library, don't implement from scratch)
  - Timeout handling with real examples
  - Graceful degradation (what happens if user-service is down?)
  
- Include a **debugging guide**:
  - How to test inter-service calls locally (mock vs. real)
  - Common port conflicts
  - Logging across services

- Add a **scenario exercise**: "Activity-service tries to log for a user that doesn't exist — trace what happens"

**Why**: Resilience patterns are practical and show why Kafka/RabbitMQ matter later.

---

### 4. Add Module Pacing & Logistics

**Requests**:
- Add a **timing breakdown per section** in each exercise.md
- Include a **"if you're falling behind" section** per module with what to skip/defer
- Add a **"what to demonstrate at the end"** checklist:
  - All 3 services running
  - One end-to-end flow (create user → create game → log activity → validate)
  - Tests passing
  - All endpoints responding via curl/Postman

---

### 5. Simplify Prerequisites & Setup

**Requests**:
- Create a **`SETUP.md`** file with:
  - Python 3.12+ installation (with version check script)
  - One-command venv setup for all 3 services
  - Pre-commit hooks to catch common issues (lint, test)
  - Troubleshooting section for WSL2/Docker Desktop/ARM Macs
  
- **Remove Node.js requirement** for the 30-hour version (notification-service is Module 4+)
- Provide a **Docker-free SQLite backup** (already there, but emphasize it)

---

### 6. Create a Quick Reference Sheet

**Requests**:
- Add `QUICK_REFERENCE.md` with:
  - Command cheatsheet (venv setup, run service, run tests, run migrations)
  - Port assignments (user: 8001, game: 8002, activity: 8003)
  - Common curl commands for testing
  - SQLite inspection commands
  - How to reset a service's database (drop DB, re-migrate)

---

### 7. Office Hours / Q&A Template

**Requests**:
- Add a `COMMON_QUESTIONS.md` with anticipated blockers:
  - "My service won't start" → check ports, requirements.txt, venv
  - "Migration failed" → show alembic troubleshooting
  - "httpx call hangs" → timeout configuration
  - "Tests pass locally but fail in CI" → async test setup

---

## Proposed Folder Structure

```
.
├── README.md (existing, keep as-is or minor edits)
├── COURSE_ADAPTATION_30H.md (this file)
├── SETUP.md (new)
├── QUICK_REFERENCE.md (new)
├── COMMON_QUESTIONS.md (new)
├── modules/
│   ├── module-01/
│   │   ├── exercise.md (compressed, with visual diagram)
│   │   └── reference-architecture.txt (ASCII diagram)
│   ├── module-02/
│   │   ├── exercise.md (updated with templates section)
│   │   ├── starter-template/ (new)
│   │   │   ├── cookiecutter.json
│   │   │   └── {{cookiecutter.service_name}}/
│   │   └── user-service-worked-example/ (new, scaffold only)
│   └── module-03/
│       ├── exercise.md (simplified, gRPC → reading)
│       ├── RESILIENCE_PATTERNS.md (new)
│       └── debugging-checklist.md (new)
├── services/ (empty, students build here)
└── _templates/ (new)
    ├── requirements.txt (pinned versions)
    ├── .env.example
    └── common-mistakes.md
```

---

## Success Criteria for Redesign

By the end of the 30-hour course, students should be able to:

1. ✅ **Design**: Explain why microservices exist and identify bounded contexts
2. ✅ **Build**: Create a FastAPI service with SQLAlchemy models, Pydantic schemas, and tests
3. ✅ **Integrate**: Make one service call another with proper error handling
4. ✅ **Deploy locally**: Run 3 services + SQLite, no Docker, all ports working
5. ✅ **Understand limits**: Articulate why sync REST breaks down and what asynchronous messaging solves

---

## Defer to Future Curriculum

The following belong in a **Module 4–10 sequel course** (30–40h):
- Docker & Docker Compose
- Kafka & RabbitMQ (async messaging)
- Keycloak (auth)
- Jaeger (distributed tracing)
- Grafana (metrics)
- GitHub Actions (CI/CD)
- Circuit breakers (deep dive)
- API Gateway (Traefik)

---

## Estimated Time Savings

| Task | Original Time | Adapted Time | Savings |
|------|---------------|--------------|---------|
| Scaffolding services | 4–5h | 30min (template) | 4h |
| Module 1 design | 2h | 30min | 1.5h |
| gRPC (Module 3) | 3h | Reading only | 3h |
| Infrastructure setup | 5h | N/A | 5h |
| Buffer for debugging | 3h | 4–6h | —1h (but more support) |
| **Total** | **70h** | **~30h** | **40h** |

---

## Next Steps for Instructor

1. **Validate this scope** with EPITA stakeholders
2. **Create starter templates** (cookiecutter or shell scripts)
3. **Audit exercise.md files** for timing accuracy
4. **Record 1–2 walkthroughs** (15–20 min) for Modules 2–3 bottlenecks
5. **Plan office hours** around Module 2 (SQLAlchemy) and Module 3 (httpx debugging)
6. **Create a final demo script** showing all 3 services working end-to-end

---

## Feedback for Claude AI

If you're using this to guide an AI rewrite, emphasize:
- **Remove infrastructure chapters entirely** (Docker, Kafka, etc.)
- **Add scaffolding and templates**
- **Compress theory; emphasize hands-on building**
- **Include troubleshooting at every step**
- **Add pacing guidance** (time-box exercises, offer shortcuts)
- **Make the end-to-end demo concrete** (actual curl commands, expected output)

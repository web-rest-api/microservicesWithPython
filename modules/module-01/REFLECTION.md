## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: **\*\***\_\_\_**\*\***
**Branch**: `module-01/<team-name>`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_

---Splitting the monolith into separate services makes the system easier to manage and maintain. For developers, changing one service becomes safer because it does not risk breaking unrelated parts of the application. For deployment teams, each service can be updated independently without redeploying the entire system. For users, failures are more isolated, meaning one broken service does not necessarily take down the whole platform

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_

---We decided to separate the activity-service from the logging-service. The activity-service is responsible for gameplay actions, while the logging-service only stores logs and audit records. If both services were merged together, gameplay performance could be affected whenever logging becomes slow or unavailable. Keeping them separate also makes the system easier to scale and maintain because logging can grow independently from gameplay activity.

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_

---Communication between components was simpler in the monolith because everything was inside the same application and database. In a distributed system, services must communicate over the network using REST APIs or async events, which adds complexity, latency, and more points of failure.

_Keep this file. You will refer back to it during the oral presentation._

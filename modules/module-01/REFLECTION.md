## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: BUI_Nhat
**Branch**: `module-01/BUI_Nhat`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_
Splitting the monolith into microservices solves deployment and maintenance problems.
In a monolith, changing one feature can require redeploying the whole application and risks breaking unrelated parts of the system. With microservices, services like activity tracking, notifications, or recommendations can evolve independently.
For developers, this means smaller and easier-to-manage codebases. For deployment teams, services can scale independently depending on demand. For users, failures become more isolated. If the notification service crashes, the rest of the platform can still continue working.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_
We separated the activity-service from the logging-service because they have different responsibilities.
The activity-service handles live gameplay and social interactions, which must stay fast and responsive. The logging-service focuses on compliance, GDPR consent, and audit records.
If these services were merged together, every gameplay action would depend on logging and compliance checks, making the system slower and more tightly coupled. Keeping them separate allows each service to evolve independently.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_
In the monolith, a request stayed inside one application, making it easier to trace errors. In the distributed system, one user action can travel through several services and RabbitMQ queues.
This makes monitoring, observability, and tracing much more important because failures can happen asynchronously across multiple services.

---

_Keep this file. You will refer back to it during the oral presentation._

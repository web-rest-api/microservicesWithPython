## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: veena
**Branch**: `module-01/veena
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_------The monolith became difficult to maintain because everything was tightly connected. A small change in one feature could accidentally break another part of the system. Splitting services makes it easier for developers to work independently and deploy changes without affecting the entire application.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_--------separated the notification-service from the activity-service because notifications are not part of the core activity logic. If notifications fail, users should still be able to log activities normally. Keeping them separate improves reliability and scalability.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_-------------------The monolith was simpler to run because everything existed in one application and one database. In the microservices design, communication between services becomes more complex and debugging is harder because requests move across multiple services.

---

_Keep this file. You will refer back to it during the oral presentation._

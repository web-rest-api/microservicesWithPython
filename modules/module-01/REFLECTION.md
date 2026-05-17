## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: Bahjat
**Branch**: `module-01/<bahjat>`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> Splitting the app solves the problem of deployment crashes and tight coupling. From a user's perspective, if the Game Library goes offline because of a bug or an update, the whole platform doesn't crash. They can still log in, view their profile, and chat with friends because the Identity and Activity services are running independently.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

>I separated the Activity service from the Notification service. In the monolith, these were tightly coupled, meaning when a user logged a game, the system paused to write notifications for all their friends before finishing the request. By separating them and using an async event, logging an activity is instant, and notifications are processed safely in the background.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

>Data querying is much harder now. In the monolith, if I wanted to show an activity feed, I could just write a single SQL JOIN to get the user's name, the game title, and the activity. Now, that data is locked in three different databases, requiring multiple network calls between services just to render one page.

---

_Keep this file. You will refer back to it during the oral presentation._

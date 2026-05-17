# Module 2 — Reflection

**Team name**: Bahjat
**Branch**: `module-02/<bahjat>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> Splitting the code into layers protects the application from massive rewrites. If we decide to swap from SQLite to PostgreSQL later, we only have to update the repository.py and database.py files. The routing (routes.py) and business logic (service.py) don't care what database is used, so they remain completely untouched. It also makes testing easier because you can test business logic without needing a live database.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> If the Activity Service was allowed to write directly to the games table in the Game Service database, it might bypass important validation rules (like adding a game without a cover_url). Even worse, if the Game Service team updates their database schema (like changing the column name title to game_name), the Activity Service's hardcoded SQL query would instantly break and crash without the Game Service team even knowing why.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

>The cost is massive boilerplate. To do a simple SELECT * FROM games, you have to write code across five different files, which feels incredibly slow for a basic CRUD app. This complexity only pays off when the app scales — when you start adding caching, role-based permissions, or external API calls, having dedicated layers keeps the codebase from turning into spaghetti.

---

*Keep this file. You will refer back to it during the oral presentation.*

# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/<team-name>`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

For each bounded context you identify, fill in the table:
| Bounded Context | Responsibilities                                         | Owned Entities             | Team           |
| --------------- | -------------------------------------------------------- | -------------------------- | -------------- |
| Identity        | Manages who users are, handles registration and profiles | User, Session              | Platform       |
| Game Library    | Manages the game catalog and game details                | Game, Genre                | Content        |
| Activity        | Tracks player activity and gameplay events               | Activity, MatchHistory     | Analytics      |
| Notification    | Sends emails, alerts, and real-time notifications        | Notification, QueueMessage | Communication  |
| Logging         | Stores system logs and audit events                      | LogEntry, AuditRecord      | Infrastructure |


There is no single correct answer: what matters is that you can justify each row.

---

## Task 2 — Define service contracts _(~30 min)_

For each pair of services that need to communicate, define:

- **Direction**: A → B
- **Trigger**: what causes the call
- **Protocol**: REST or event (async)
- **Payload**: key fields exchanged

Example:

```
activity-service → logging-service
Trigger: an activity is logged
Protocol: RabbitMQ message (async — why not REST here?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

---Service Contracts
gateway → identity-service
Trigger: user logs in
Protocol: REST
Payload: { email, password }

activity-service → logging-service
Trigger: gameplay activity recorded
Protocol: RabbitMQ event (async)
Payload: { activity_id, user_id, action, timestamp }

game-library-service → notification-service
Trigger: new game added
Protocol: RabbitMQ event (async)
Payload: { game_id, title, release_date }

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

---
                    +-------------+
                    |   Gateway   |
                    +-------------+
                      /    |    \
                     /     |     \
                    v      v      v

          +-------------+  +-------------+
          | Identity    |  | Game Library|
          | Service     |  | Service     |
          +-------------+  +-------------+
                 |                 |
                 |                 |
                 v                 v

          +-------------+   - - - - - - - - -
          | Activity    | - - > Notification |
          | Service     |     (RabbitMQ)     |
          +-------------+   - - - - - - - - -

                 |
                 |
                 v

          +-------------+
          | Logging     |
          | Service     |
          +-------------+

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?
--Node.js is well suited for real-time communication and event-driven systems.
This shows that microservices can use different technologies depending on the needs of each service.

2. What is the risk of `activity-service` calling `logging-service` synchronously — why might you prefer an async event instead?

3. Why does `logging-service` need a GDPR consent check before recording any activity?

You do not need to write these answers down — they are warm-up for your REFLECTION.md.

---

## Minimum to submit this branch

- [ ] Bounded context table filled in (at least 4 services justified)
- [ ] At least 3 service contracts defined
- [ ] Service map committed (sketch, photo, or ASCII)
- [ ] `REFLECTION.md` completed and committed

The map does not need to be perfect. It needs to be yours.

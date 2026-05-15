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

| Bounded Context        | Responsibilities                                                              | Owned Entities                           | Team        |
| ---------------------- | ----------------------------------------------------------------------------- | ---------------------------------------- | ----------- |
| Identity / Auth        | Handles registration, login, JWT authentication, and password security        | User, Credentials, Session, RefreshToken | Platform    |
| Profile Service        | Manages public user profiles and social information                           | Profile, Avatar, Bio, FriendRelation     | Social      |
| Game Library           | Stores game information and users’ game collections                           | Game, Genre, UserLibraryEntry            | Discovery   |
| Activity Service       | Tracks gameplay activity and publishes activity events                        | Activity, PlaySession, StatusUpdate      | Engagement  |
| Recommendation Service | Generates personalized game recommendations                                   | Recommendation, RecommendationScore      | Discovery   |
| Notification Service   | Sends notifications to users about social activity                            | Notification, DeliveryStatus             | Platform    |
| Logging Service        | Stores GDPR-compliant logs and consent tracking                               | ConsentRecord, ActivityLog, AuditEvent   | Compliance  |

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

### 1. Activity Service → Logging Service

- **Direction:** `activity-service → logging-service`
- **Trigger:** User starts/stops playing a game
- **Protocol:** RabbitMQ event (async)
- **Payload:**

```json
{
  "activity_id": "a123",
  "user_id": "u42",
  "game_id": "g88",
  "action": "started_playing",
  "timestamp": "2026-05-15T14:20:00Z"
}
```

**Why async?**

Logging should not block gameplay actions. If logging becomes slow or unavailable, the activity service should still work normally.

---

### 2. Activity Service → Notification Service

- **Direction:** `activity-service → notification-service`
- **Trigger:** Friend starts playing a game
- **Protocol:** RabbitMQ event (async)
- **Payload:**

```json
{
  "user_id": "u42",
  "friend_ids": ["u10", "u11"],
  "game_id": "g88",
  "event": "friend_started_game",
  "timestamp": "2026-05-15T14:20:00Z"
}
```

**Why async?**

Notifications are background tasks and should not slow down the user experience.

---

### 3. Gateway → Auth Service

- **Direction:** `gateway → auth-service`
- **Trigger:** User login or JWT validation
- **Protocol:** REST (synchronous)
- **Payload:**

```json
{
  "username": "player1",
  "password": "********"
}
```

**Response:**

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Why REST?**

Authentication requires an immediate response before the request can continue.

---

### 4. Activity Service → Recommendation Service

- **Direction:** `activity-service → recommendation-service`
- **Trigger:** New gameplay activity
- **Protocol:** RabbitMQ event (async)
- **Payload:**

```json
{
  "user_id": "u42",
  "game_id": "g88",
  "playtime_minutes": 120,
  "genre": "RPG"
}
```

**Why async?**

Recommendations do not need to update instantly and can be processed in the background.

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

---

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

```text
                        +----------------+
                        |    CLIENTS     |
                        +----------------+
                                 |
                                 v
                       +------------------+
                       |      GATEWAY     |
                       | JWT / Routing    |
                       +------------------+
                          |      |      |
                REST      |      |      | REST
                          v      v      v
                 +---------+  +-------------+
                 |  AUTH   |  |   PROFILE   |
                 +---------+  +-------------+
                        |
                        |
                        v
                 +---------------+
                 | GAME LIBRARY  |
                 +---------------+
                        |
                        | REST
                        v
                 +---------------+
                 |   ACTIVITY    |
                 +---------------+
                    /        \
           RabbitMQ          RabbitMQ
                /                \
               v                  v
      +----------------+   +----------------+
      | NOTIFICATION   |   |    LOGGING     |
      |   Node.js      |   | Flask + GDPR   |
      +----------------+   +----------------+
                \
                 \ RabbitMQ
                  \
                   v
          +-------------------+
          | RECOMMENDATIONS   |
          +-------------------+
```

Legend:

- Solid arrows = synchronous REST
- Dashed/event arrows = async RabbitMQ events

---

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?
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

# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*

The gateway exists to simplify communication between the client and the microservices. Instead of the client needing to know where every service is running, the client only communicates with a single entry point.

Without a gateway, the frontend would need to manage multiple service URLs and ports such as user-service on port 8001, game-service on port 8002, and activity-service on port 8003. If a service changed location, port, or infrastructure, every client application would also need to be updated.

The gateway centralizes routing and hides the internal architecture from the client. It also makes it easier to add authentication, logging, rate limiting, or monitoring later without changing every service individually.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:*

The user validation call is critical because an activity should never be created for a user that does not exist. If this validation fails, invalid data could be permanently stored in the database. That is why the service retries the request and blocks activity creation if the user cannot be validated.

The game lookup is different because it is only used for optional enrichment of the response. Even if the game-service is unavailable, the activity itself is still valid and can be saved correctly. In that case, the system degrades gracefully by returning `"game": null` instead of failing completely.

For the user, this means activity creation still works even when the game-service is temporarily down, which improves resilience and availability.

---


## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*

The main risk of synchronous service chains is that the overall system becomes slower and more fragile. Every additional service call increases latency and creates another possible point of failure.

If one service in the chain becomes slow, the entire request slows down because each service waits for the previous one to finish. For example, if the slowest service takes 3 seconds to respond, the user may experience long delays before receiving a final response.

If one service becomes unavailable entirely, it can also affect multiple other services and create cascading failures throughout the system. This is one of the main tradeoffs of microservice architectures compared to monolithic applications.

---

*Keep this file. You will refer back to it during the oral presentation.*

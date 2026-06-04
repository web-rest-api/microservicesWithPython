# Module 4 — Reflection

**Team name**: _______________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:* By not waiting for notification-service, activity-service can save the activity and respond to the user immediately. This makes the system faster and prevents activity creation from failing just because notifications are slow or temporarily unavailable.

Notification-service also benefits because it can process messages at its own pace. If there is a spike in traffic, messages can stay in RabbitMQ until the service is ready to consume them. If notification-service goes down for a short time, the messages remain in the queue and can be processed when the service comes back online.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:* Using a broker is more reliable than making a direct HTTP call for notifications. With HTTP, activity-service would have to wait for notification-service to respond, and activity creation could fail if notification-service was slow or offline.

RabbitMQ acts as a buffer between the services. Activity-service only needs to publish a message and continue. If notification-service crashes or becomes overloaded, the messages remain in the queue instead of being lost. This reduces coupling between the services and improves resilience.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:* With asynchronous messaging, users do not get immediate confirmation that a notification was actually delivered. They only know that the activity was created successfully. If the notification is never processed, the user may not notice until they realize they never received it.

As a developer, I also lose immediate visibility because there is no direct success or failure response from notification-service. Instead, I have to rely on monitoring tools, logs, queue metrics, and dead-letter queues to detect problems. The tradeoff is better scalability and reliability, but less immediate feedback about whether downstream processing succeeded.

---

*Keep this file. You will refer back to it during the oral presentation.*

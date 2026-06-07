# Module 4 — Reflection

**Team name**: ______fred_________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:*

---so basically activity-service before had to wait for everything to finish before it could send back a response to the user, now it just drops the message in the queue and immediately says "ok done" without waiting for anyone to pick it up. this means if notification-service is super slow or even completely down, the user still gets a fast response and the activity still gets saved. notification-service on the other side can just process messages whenever it wants, if it gets 1000 notifications at once it can go through them one by one at its own speed instead of crashing because too many requests came in at the same time.

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:*

---if we called notification-service directly over HTTP like we did for user validation, then if notification-service crashes in the middle of sending, the whole request fails or hangs. also if its slow, the user has to wait longer just because of notifications which has nothing to do with saving the activity. the broker fixes this because the message sits in the queue safely even if notification-service is down, when it comes back up it just picks up where it left off. with direct HTTP if the service is down the message is just gone.

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:*

---yeah this is the annoying part of async, you basically have no idea if the notification actually got delivered or not. from the user side they might just never see the notification and have no idea why. from the developer side you would have to check the RabbitMQ UI manually or look at logs in notification-service to see if messages are being consumed. you lose the immediate feedback you get with REST where you know right away if it worked or failed. to fix this properly you would need to add some kind of logging or monitoring that tracks when a message was picked up and processed, but that adds more complexity.

*Keep this file. You will refer back to it during the oral presentation.*

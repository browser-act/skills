---
description: Trigger-action rules for browser automation
---

**Policy structure — each policy has these fields:**

| Field | Description |
|-------|-------------|
| `enabled` | `true` = active, `false` = skip this policy entirely |
| `trigger` | Condition to evaluate. When this condition is met, execute the action |
| `action` | What to do when triggered (see actions below) |
| `note` | Extra context to help you judge edge cases |

**Available actions:**

| Action | Behavior |
|--------|----------|
| `Request human assist` | Stop automation, call `human-assist-url` (see Human Assist section in SKILL.md), and wait for the user to finish before continuing |

---

## credential-login

- enabled: true
- trigger: You need to enter credentials (username, password, MFA code) but the user has not provided them
- action: Request human assist
- note: Do NOT guess or fill credentials. If the user provided credentials, cookies are injected, or the task is to operate on the page, proceed normally.

## captcha-unsolvable

- enabled: true
- trigger: You attempted solve-captcha but it did not succeed
- action: Request human assist
- note: Let the user solve it manually.

## operation-stuck

- enabled: true
- trigger: You have tried multiple approaches to complete an action but none work
- action: Request human assist
- note: Do not keep retrying — hand off to the user.

## payment-confirmation

- enabled: true
- trigger: Reached a payment or checkout page where money will be charged
- action: Request human assist
- note: User wants to review the order before completing purchase


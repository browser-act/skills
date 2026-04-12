---
description: Trigger-action rules for browser automation
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


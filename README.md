# 🟢 Unraid Release Watcher

A lightweight Docker service that polls the official Unraid announcements feed and notifies you via [Apprise](https://github.com/caronc/apprise) when:

1. A new **stable Unraid OS release** is announced (beta/rc/pre/alpha excluded).  
2. The current stable release has been out for a configurable number of days (default **30**) — reminding you it’s time to update.

---

## ✨ Features

- Detects **new stable** Unraid OS releases.
- Sends notification immediately via Apprise.
- Sends **one** reminder after a configurable delay (`REMINDER_DELAY_DAYS`).
- Configurable polling interval (`POLL`).
- Stores persistent state in `/data/state.json`.
- Built-in `/health` endpoint for Docker healthchecks.
- Logs directly to stdout for `docker logs`.
- `--simulate` or `SIMULATE=true` to send a test notification and exit.
- Includes unit tests and CI workflow for linting, testing, and Docker build.

---

## 🚀 Quick Start

### With Docker CLI

```bash
docker run -d --name unraid-watcher \
  -v /mnt/user/appdata/unraid-watcher:/data \
  -e APPRISE_URLS="mailto://you@example.org" \
  -e POLL="1h" \
  -e REMINDER_DELAY_DAYS="30" \
  ghcr.io/peglah/unraid-watcher:latest
```

---

## 🤖 About This Project

This project was collaboratively designed and implemented with the assistance of AI.
All code, documentation, and automation workflows were generated and refined through human oversight to ensure clarity, correctness, and maintainability.

The repository is open under the [MIT License](./LICENSE) — you are free to use, modify, and redistribute it as you would any other open-source project.

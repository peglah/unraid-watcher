FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY README.md /app/README.md

RUN mkdir -p /data
EXPOSE 8000

ENV FEED_URL="https://forums.unraid.net/forums/forum/7-announcements.xml"
ENV APPRISE_URLS="mailto://you@example.org"
ENV POLL="1h"
ENV REMINDER_DELAY_DAYS="30"
ENV STATE_FILE="/data/state.json"
ENV SIMULATE="false"

HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3   CMD curl -f http://127.0.0.1:8000/health || exit 1

ENTRYPOINT ["python", "-m", "app.main"]

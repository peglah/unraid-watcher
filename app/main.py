import argparse
import logging
import time
import re
import signal
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import os

from .feed import parse_feed_from_url, latest_stable_entry
from .state import State
from .notifier import send_apprise_notification
from .web import run_app

logger = logging.getLogger("unraid-watcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DEFAULT_FEED = "https://forums.unraid.net/forums/forum/7-announcements.xml"
DEFAULT_POLL = "1h"

def parse_interval(s: str) -> int:
    s = s.strip().lower()
    m = re.match(r"^(\d+)(min|m|h|d|mo)$", s)
    if not m:
        raise ValueError("Invalid interval, use e.g. 15m, 1h, 7d, 1mo")
    val = int(m.group(1))
    unit = m.group(2)
    if unit in ("min", "m"):
        return val * 60
    if unit == "h":
        return val * 3600
    if unit == "d":
        return val * 86400
    if unit == "mo":
        return val * 30 * 86400
    raise ValueError("unsupported unit")

def try_fetch(url, retries=3):
    delay = 1
    for attempt in range(1, retries + 1):
        try:
            return parse_feed_from_url(url)
        except Exception as e:
            logger.warning("fetch attempt %s failed: %s", attempt, e)
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("failed to fetch feed after retries")

def should_send_reminder(last_published_iso, reminder_sent_for, last_id, delay_days=30):
    if not last_published_iso:
        return False
    try:
        pub = dateparser.parse(last_published_iso)
    except Exception:
        return False
    now = datetime.now(pub.tzinfo) if pub.tzinfo else datetime.utcnow()
    if (now - pub) >= timedelta(days=delay_days):
        return reminder_sent_for != last_id
    return False

def main_loop(feed_url, state_path, apprise_cfg, poll_seconds, simulate=False):
    state = State(state_path)
    run_app()

    if simulate:
        send_apprise_notification(apprise_cfg, "Unraid Watcher: test", "This is a simulated test notification.")
        logger.info("Simulate mode: sent test notification; exiting.")
        return

    logger.info("Starting poll loop: feed=%s interval=%ss state=%s", feed_url, poll_seconds, state_path)
    stop = False
    def _sig(signum, frame):
        nonlocal stop
        logger.info("Received signal %s, stopping...", signum)
        stop = True
    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)

    while not stop:
        try:
            feed = try_fetch(feed_url)
            latest = latest_stable_entry(feed)
            st = state.get()
            last_id = st.get('last_stable_id')
            last_pub_iso = st.get('last_stable_published')
            reminder_sent_for = st.get('reminder_sent_for')

            if latest:
                latest_id = latest.get('id')
                latest_pub = latest.get('published')
                latest_pub_iso = latest_pub.isoformat() if latest_pub else None

                if latest_id != last_id:
                    title = f"Unraid stable release: {latest.get('title')}"
                    body = f"{latest.get('title')}\n\n{latest.get('link')}\n\nPublished: {latest_pub_iso}"
                    send_apprise_notification(apprise_cfg, title, body)
                    state.set_last_stable(latest_id, latest_pub_iso)
                    logger.info("New stable release announced: %s", latest.get('title'))
                elif should_send_reminder(
                        last_pub_iso,
                        reminder_sent_for,
                        last_id,
                        delay_days=float(os.environ.get("REMINDER_DELAY_DAYS", "30"))
                    ):
                    title = "Unraid update reminder: 30 days since last stable release"
                    body = f"It's been 30 days since the last stable Unraid release ({last_pub_iso}). Consider planning your OS update.\n\nLink: {latest.get('link')}"
                    send_apprise_notification(apprise_cfg, title, body)
                    state.set_reminder_sent(last_id)
                    logger.info("30-day reminder sent for release %s", last_id)
        except Exception:
            logger.exception("Error in poll loop iteration")
        for _ in range(int(poll_seconds)):
            if stop:
                break
            time.sleep(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--feed", default=os.environ.get("FEED_URL", DEFAULT_FEED))
    p.add_argument("--state", default=os.environ.get("STATE_FILE", "/data/state.json"))
    p.add_argument("--apprise", default=os.environ.get("APPRISE_URLS", "mailto://you@example.org"))
    p.add_argument("--poll", default=os.environ.get("POLL", DEFAULT_POLL))
    p.add_argument("--simulate", action="store_true")
    args = p.parse_args()

    simulate_env = os.environ.get("SIMULATE", "false").lower() == "true"
    simulate_flag = args.simulate or simulate_env

    apprise_cfg = [u for u in args.apprise.split(",") if u.strip()]
    poll_seconds = parse_interval(args.poll)
    main_loop(args.feed, args.state, apprise_cfg, poll_seconds, simulate=simulate_flag)

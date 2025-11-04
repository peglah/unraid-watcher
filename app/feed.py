import re
import feedparser
from dateutil import parser as dateparser
import logging
from typing import Optional, Dict, Any

STABLE_EXCLUDE_RE = re.compile(r"(beta|rc|pre|alpha)", re.IGNORECASE)
logger = logging.getLogger(__name__)


def is_stable_title(title: str) -> bool:
    return not bool(STABLE_EXCLUDE_RE.search(title))


def parse_feed_from_url(url: str) -> Any:
    d = feedparser.parse(url)
    if d.bozo and d.bozo_exception:
        logger.debug("feedparser.bozo_exception: %s", d.bozo_exception)
    return d


def latest_stable_entry(feed_parsed: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    best = None
    for e in feed_parsed.get('entries', []):
        title = e.get('title', '')
        if not is_stable_title(title):
            continue
        pub = None
        if 'published' in e:
            try:
                pub = dateparser.parse(e['published'])
            except Exception:
                pub = None
        rec = {
            'title': title,
            'link': e.get('link'),
            'published': pub,
            'id': e.get('id') or e.get('guid') or e.get('link')
        }
        if best is None:
            best = rec
        else:
            if pub and best.get('published'):
                if pub > best['published']:
                    best = rec
            elif pub and not best.get('published'):
                best = rec
    return best

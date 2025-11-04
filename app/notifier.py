import apprise
import logging

logger = logging.getLogger(__name__)


def send_apprise_notification(apprise_urls, title, body):
    a = apprise.Apprise()
    for url in apprise_urls:
        a.add(url.strip())
    ok = a.notify(title=title, body=body)
    logger.info("Apprise notify result: %s", ok)
    return ok

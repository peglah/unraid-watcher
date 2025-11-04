import json
from pathlib import Path
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DEFAULT_STATE: Dict[str, Optional[str]] = {
    "last_stable_id": None,
    "last_stable_published": None,
    "reminder_sent_for": None
}


class State:
    def __init__(self, path: str = "/data/state.json"):
        self.path = Path(path)
        self._state: Dict[str, Optional[str]] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                j = json.loads(self.path.read_text())
            except Exception:
                logger.exception("Failed reading state file, resetting.")
                j = DEFAULT_STATE.copy()
        else:
            j = DEFAULT_STATE.copy()
        for k, v in DEFAULT_STATE.items():
            j.setdefault(k, v)
        self._state = j

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._state, indent=2))

    def get(self) -> Dict[str, Optional[str]]:
        return self._state

    def set_last_stable(self, stable_id: str, published_iso: Optional[str]):
        self._state['last_stable_id'] = stable_id
        self._state['last_stable_published'] = published_iso
        self._state['reminder_sent_for'] = None
        self.save()

    def set_reminder_sent(self, stable_id: str):
        self._state['reminder_sent_for'] = stable_id
        self.save()

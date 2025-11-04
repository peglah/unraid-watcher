from flask import Flask, jsonify
import threading
import logging

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


def run_app(host="0.0.0.0", port=8000):
    app = create_app()
    t = threading.Thread(
        target=app.run,
        kwargs={
            'host': host,
            'port': port,
            'threaded': True
        },
        daemon=True
    )
    t.start()
    logger.info("Health endpoint started on %s:%s", host, port)

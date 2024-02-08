import click
import logging
from os import getenv as os_getenv
from flask import Flask
from flask_cors import CORS

from core.challenge_api import api as backend_challenge_api


def create_app():
    """
    Create a Flask app with the backend_challenge_api blueprint.
    Returns:
        Flask: The Flask app
    """
    app = Flask("Backend Challenge API")
    CORS(app)
    app.register_blueprint(backend_challenge_api, url_prefix="/backend")

    log_level = os_getenv('LOG_LEVEL', 'DEBUG')

    app.logger.setLevel(getattr(logging, log_level))
    return app


@click.group(name="api-server")
def cli():
    pass


# noinspection HttpUrlsUsage
@cli.command(name="vehicle-features", help="Generate comparison images.")
@click.option(
    "--host",
    "host",
    help="The hostname to listen on.",
    default="127.0.0.1",
    type=str,
)
@click.option(
    "--port",
    "port",
    help="The port of the webserver.",
    default=8080,
    type=int,
)
def vehicle_features(host: str, port: int):
    """
    Serves an API with `Flask`.
    http://<host>:<port>/backend/

    Args:
        host: The hostname to listen on.
        port: The port of the webserver.
    """
    app = create_app()
    app.run(host=host, port=port, debug=True)

import logging

from connexion.exceptions import Unauthorized
from flask import abort
from flask import current_app as app

from . import UpstreamProviderError, provider

logger = logging.getLogger(__name__)


def search(body):
    try:
        data = provider.search(body["query"])
    except UpstreamProviderError as error:
        logger.error(f"Upstream search error: {error.message}")
        abort(502, error.message)
    except AssertionError as error:
        logger.error(f"SnowFlake config error: {error}")
        abort(502, f"SnowFlake config error: {error}")

    return {"results": data}, 200, {"X-Connector-Id": app.config.get("APP_ID")}


def apikey_auth(token):
    if token != str(app.config.get("CONNECTOR_API_KEY")):
        raise Unauthorized()
    # successfully authenticated
    return {}

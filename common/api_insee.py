import base64
import logging

import redis as r
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

redis = r.from_url(settings.REDIS_URL, decode_responses=True)


def get_token_sirene():
    if not settings.SIRET_API_KEY or not settings.SIRET_API_SECRET:
        logger.warning("skipping siret token fetching because key and secret env vars aren't set")
        return
    token_redis_key = f"{settings.REDIS_PREPEND_KEY}SIRET_API_TOKEN"
    if redis.exists(token_redis_key):
        return redis.get(token_redis_key)

    base64Cred = base64.b64encode(bytes(f"{settings.SIRET_API_KEY}:{settings.SIRET_API_SECRET}", "utf-8")).decode(
        "utf-8"
    )
    token_data = {"grant_type": "client_credentials", "validity_period": 604800}
    token_headers = {"Authorization": f"Basic {base64Cred}"}
    token_response = requests.post("https://api.insee.fr/token", data=token_data, headers=token_headers)
    if token_response.ok:
        token_response = token_response.json()
        token = token_response["access_token"]
        expiration_seconds = 60 * 60 * 24
        redis.set(token_redis_key, token, ex=expiration_seconds)
        return token
    else:
        logger.warning(f"token fetching failed, code {token_response.status_code} : {token_response}")

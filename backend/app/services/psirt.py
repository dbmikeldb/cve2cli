# backend/app/services/psirt.py

import httpx

from urllib.parse import urlencode
from typing import Optional

from backend.app.core.config import settings
from backend.app.core.logging import api_logger, app_logger, auth_logger, cve_logger
from backend.app.utils.data_formatting import format_json

client_id = settings.cisco_client_id
client_secret = settings.cisco_client_secret

AUTH_URL = "https://id.cisco.com/oauth2/default/v1/token"
PSIRT_CVE_URL = "https://apix.cisco.com/security/advisories/v2/cve/"
PSIRT_ADVISORY_URL = "https://apix.cisco.com/security/advisories/v2/advisory/"


async def get_access_token() -> str:
    app_logger.debug("Function 'get_access_token' beginning.")

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    auth_logger.debug("Requesting Cisco access token.")

    try:
        async with httpx.AsyncClient() as client:
            api_logger.debug(f"POST {AUTH_URL} | Headers: {headers} | Payload: {data}")
            resp = await client.post(AUTH_URL, data=urlencode(data), headers=headers)
            resp.raise_for_status()
    except httpx.HTTPStatusError as http_err:
        auth_logger.error(f"HTTP error while getting access token: {http_err.response.status_code} {http_err.response.text}")
        raise
    except Exception as err:
        auth_logger.exception("Unexpected error while getting access token")
        raise

    token = resp.json().get("access_token")
    if not token:
        auth_logger.warning("Access token not found in response!")
    else:
        auth_logger.info("Access token successfully retrieved.")

    app_logger.debug("Exiting 'get_access_token'.")
    return token


async def _fetch_psirt(url: str, token: str) -> Optional[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            cve_logger.error(f"HTTP error fetching {url}: {e}")
        except httpx.RequestError as e:
            cve_logger.error(f"Request error fetching {url}: {e}")
        return None


async def fetch_cve_data(cve_id: str) -> Optional[dict]:
    app_logger.debug(f"Starting 'fetch_cve_data' for CVE ID: {cve_id}")
    try:
        token = await get_access_token()
        data = await _fetch_psirt(f"{PSIRT_CVE_URL}{cve_id}", token)
        if data:
            pretty = format_json(data)
            cve_logger.debug(f"CVE Data: {pretty}")
            return pretty
        app_logger.warning(f"CVE ID {cve_id} not found or no data.")
        return None
    except Exception as e:
        app_logger.error(f"Unexpected error in 'fetch_cve_data' for {cve_id}: {e}")
        raise
    finally:
        app_logger.debug(f"Exiting 'fetch_cve_data' for CVE ID: {cve_id}")


async def fetch_advisory_data(advisory_id: str) -> Optional[dict]:
    app_logger.debug(f"Starting 'fetch_advisory_data' for Advisory ID: {advisory_id}")
    try:
        token = await get_access_token()
        data = await _fetch_psirt(f"{PSIRT_ADVISORY_URL}{advisory_id}", token)
        if data:
            pretty = format_json(data)
            cve_logger.debug(f"Advisory Data: {pretty}")
            return pretty
        app_logger.warning(f"Advisory ID {advisory_id} not found or no data.")
        return None
    except Exception as e:
        app_logger.error(f"Unexpected error in 'fetch_advisory_data' for {advisory_id}: {e}")
        raise
    finally:
        app_logger.debug(f"Exiting 'fetch_advisory_data' for Advisory ID: {advisory_id}")

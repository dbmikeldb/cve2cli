# backend/app/services/psirt.py

import httpx
import json

from urllib.parse import urlencode
from typing import Optional

from backend.app.core.config import settings
from backend.app.core.logging import api_logger, app_logger, auth_logger
from backend.app.utils.data_formatting import format_json

client_id = settings.cisco_client_id
client_secret = settings.cisco_client_secret


AUTH_URL = "https://id.cisco.com/oauth2/default/v1/token"
PSIRT_API_URL = "https://apix.cisco.com/security/advisories/v2/cve/"


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

    auth_logger.info("Requesting Cisco access token.")

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
        auth_logger.debug("Access token successfully retrieved.")

    app_logger.debug("Exiting 'get_access_token'.")
    return token
    

async def fetch_cve_data(cve_id: str) -> Optional[dict]:
    app_logger.debug(f"Starting 'fetch_cve_data' for CVE ID: {cve_id}")

    try:
        token = await get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        api_logger.info(f"Fetching CVE data from {PSIRT_API_URL}{cve_id}")

        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PSIRT_API_URL}{cve_id}", headers=headers)

        if resp.status_code == 200:
            app_logger.debug(f"Successfully fetched CVE data for {cve_id}")
            pretty_json = format_json(resp.json())

            return pretty_json

        elif resp.status_code == 404:
            app_logger.warning(f"CVE ID {cve_id} not found (404). Returning None.")
            return None

        else:
            resp.raise_for_status()

    except httpx.HTTPStatusError as http_err:
        app_logger.error(f"HTTP error fetching CVE {cve_id}: {http_err}")
        raise

    except Exception as e:
        app_logger.error(f"Unexpected error in 'fetch_cve_data' for {cve_id}: {e}")
        raise

    finally:
        app_logger.debug(f"Exiting 'fetch_cve_data' for CVE ID: {cve_id}")

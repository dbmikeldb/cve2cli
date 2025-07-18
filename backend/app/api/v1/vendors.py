# app/api/v1/vendors.py

from fastapi import APIRouter, HTTPException

from backend.app.services.psirt import fetch_cve_data, fetch_advisory_data

router = APIRouter(prefix = "/vendor", tags=["vendor"])


@router.get("/cisco/{cve_id}")
async def get_cisco_cve(cve_id: str):
    data = await fetch_cve_data(cve_id)

    if not data:
        raise HTTPException(status_code=404,
                            detail="CVE not found in Cisco PSIRT API")
    
    return data


@router.get("/cisco/advisory/{advisory_id}")
async def get_cisco_advisory(advisory_id: str):
    data = await fetch_advisory_data(advisory_id)

    if not data:
        raise HTTPException(status_code=404,
                            detail="Advisory not found in Cisco PSIRT API")

    return data
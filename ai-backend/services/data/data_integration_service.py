"""
Data Integration Service: WRIS/INGRES/CGWB (mock-first)
"""
from typing import Optional, Dict, Any
import httpx
from config.settings import get_settings

class DataIntegrationService:
    def __init__(self) -> None:
        self.settings = get_settings()
        # Prefer mock API in dev unless disabled
        self.use_mock = bool(self.settings.USE_MOCK_SERVICES)
        self.mock_base = getattr(self.settings, 'MOCK_API_BASE', 'http://localhost:8081/api')
        # In future, real endpoints can be wired here
        self.wris_base = self.settings.WRIS_API
        self.ingres_base = self.settings.INGRES_API
        self.cgwb_base = self.settings.CGWB_API

    async def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json()

    async def groundwater_level(self, district: Optional[str] = None, block: Optional[str] = None, season: Optional[str] = None) -> Dict[str, Any]:
        if self.use_mock:
            url = f"{self.mock_base}/groundwater/level"
            params = {"district": district, "block": block, "season": season}
            return await self._get(url, params)
        # TODO: implement real call
        return {"status": "stub", "message": "real WRIS/INGRES integration not implemented"}

    async def water_quality(self, district: Optional[str] = None) -> Dict[str, Any]:
        if self.use_mock:
            url = f"{self.mock_base}/groundwater/quality"
            params = {"district": district}
            return await self._get(url, params)
        return {"status": "stub", "message": "real CGWB quality integration not implemented"}

    async def rainfall(self, district: Optional[str] = None, year: Optional[int] = None) -> Dict[str, Any]:
        if self.use_mock:
            url = f"{self.mock_base}/rainfall"
            params = {"district": district, "year": year}
            return await self._get(url, params)
        return {"status": "stub", "message": "real WRIS rainfall integration not implemented"}

    async def drilling_recommendation(self, district: Optional[str] = None) -> Dict[str, Any]:
        if self.use_mock:
            url = f"{self.mock_base}/drilling/recommendation"
            params = {"district": district}
            return await self._get(url, params)
        return {"status": "stub", "message": "real drilling advisory not implemented"}

    async def dwlr_telemetry(self, station_id: str) -> Dict[str, Any]:
        # No mock endpoint provided; return stub for now
        return {"status": "stub", "station_id": station_id}

    async def assessment_units(self, lat: float, lon: float) -> Dict[str, Any]:
        # No mock endpoint provided; return stub for now
        return {"status": "stub", "lat": lat, "lon": lon}


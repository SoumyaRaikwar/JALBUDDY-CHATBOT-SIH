"""
INGRES data endpoints for jalBuddy AI
Integrates with real INGRES API and provides caching
"""

from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Response models for INGRES data
class IngresResponse(BaseModel):
    status: str
    data: Dict[str, Any]
    timestamp: str
    
class DistrictInfo(BaseModel):
    district: str
    state: str
    geology: Optional[str] = None
    blocks_count: Optional[int] = None

@router.get("/groundwater/level")
async def get_groundwater_level(
    request: Request,
    district: str = Query(..., description="District name"),
    state: Optional[str] = Query(None, description="State name"),
    block: Optional[str] = Query(None, description="Block name"),
    season: str = Query("post_monsoon", description="Season for data")
):
    """Get groundwater level data for a district"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        data = await ingres_service.get_groundwater_level(
            district=district,
            state=state, 
            block=block,
            season=season
        )
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch groundwater level for {district}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/groundwater/quality")
async def get_water_quality(
    request: Request,
    district: str = Query(..., description="District name"),
    state: Optional[str] = Query(None, description="State name")
):
    """Get water quality data for a district"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        data = await ingres_service.get_water_quality(
            district=district,
            state=state
        )
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch water quality for {district}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rainfall")
async def get_rainfall_data(
    request: Request,
    district: str = Query(..., description="District name"),
    year: Optional[int] = Query(None, description="Year for data")
):
    """Get rainfall and recharge data for a district"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        data = await ingres_service.get_rainfall_data(
            district=district,
            year=year
        )
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch rainfall data for {district}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/drilling/recommendation")
async def get_drilling_recommendation(
    request: Request,
    district: str = Query(..., description="District name"),
    state: Optional[str] = Query(None, description="State name")
):
    """Get borewell drilling recommendations for a district"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        data = await ingres_service.get_drilling_recommendation(
            district=district,
            state=state
        )
        
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch drilling recommendation for {district}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/districts")
async def get_available_districts(request: Request):
    """Get list of available districts with groundwater data"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        districts = await ingres_service.get_available_districts()
        
        return {
            "status": "success",
            "data": districts,
            "count": len(districts)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch available districts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comprehensive/{district}")
async def get_comprehensive_data(
    request: Request,
    district: str,
    state: Optional[str] = Query(None),
    include_forecast: bool = Query(False, description="Include rainfall forecast data")
):
    """Get comprehensive groundwater data for a district"""
    try:
        ingres_service = getattr(request.app.state, 'ingres_service', None)
        if not ingres_service:
            raise HTTPException(status_code=503, detail="INGRES service not available")
        
        logger.info(f"📊 Fetching comprehensive data for {district}")
        
        # Fetch all data types concurrently
        import asyncio
        
        tasks = [
            ingres_service.get_groundwater_level(district, state),
            ingres_service.get_water_quality(district, state),
            ingres_service.get_rainfall_data(district),
            ingres_service.get_drilling_recommendation(district, state)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        comprehensive_data = {
            "district": district.title(),
            "state": state,
            "groundwater_level": results[0] if not isinstance(results[0], Exception) else None,
            "water_quality": results[1] if not isinstance(results[1], Exception) else None,
            "rainfall_data": results[2] if not isinstance(results[2], Exception) else None,
            "drilling_recommendation": results[3] if not isinstance(results[3], Exception) else None,
            "data_availability": {
                "groundwater_level": not isinstance(results[0], Exception),
                "water_quality": not isinstance(results[1], Exception), 
                "rainfall_data": not isinstance(results[2], Exception),
                "drilling_recommendation": not isinstance(results[3], Exception)
            }
        }
        
        return {
            "status": "success",
            "data": comprehensive_data,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch comprehensive data for {district}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

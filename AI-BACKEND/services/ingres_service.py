"""
INGRES API Integration Service for jalBuddy
Handles real-time groundwater data fetching with caching and fallback
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import httpx
import redis.asyncio as redis
from config.settings import get_settings

logger = logging.getLogger(__name__)

class IngresService:
    """Service for integrating with INGRES groundwater data API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client: Optional[redis.Redis] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        self.initialized = False
        
        # Determine base URL based on environment
        self.base_url = (
            self.settings.INGRES_MOCK_URL 
            if self.settings.USE_MOCK_INGRES 
            else self.settings.INGRES_BASE_URL
        )
        
    async def initialize(self):
        """Initialize INGRES service with Redis cache and HTTP client"""
        try:
            logger.info("🌊 Initializing INGRES Service...")
            
            # Initialize Redis client
            self.redis_client = redis.from_url(self.settings.REDIS_URL, decode_responses=True)
            await self.redis_client.ping()
            logger.info("✅ Redis cache connected")
            
            # Initialize HTTP client
            self.http_client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(30.0),
                headers={
                    "User-Agent": f"jalBuddy-SIH2025/{self.settings.VERSION}",
                    "Accept": "application/json"
                }
            )
            
            # Add API key if using real INGRES
            if not self.settings.USE_MOCK_INGRES and self.settings.INGRES_API_KEY:
                self.http_client.headers.update({
                    "Authorization": f"Bearer {self.settings.INGRES_API_KEY}"
                })
            
            # Test connection
            await self._test_connection()
            
            self.initialized = True
            logger.info("✅ INGRES Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ INGRES Service initialization failed: {str(e)}")
            raise
    
    async def _test_connection(self):
        """Test INGRES API connection"""
        try:
            response = await self.http_client.get("/health")
            if response.status_code == 200:
                logger.info(f"🔗 INGRES API connected: {self.base_url}")
            else:
                logger.warning(f"⚠️ INGRES API connection issue: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ INGRES API connection test failed: {str(e)}")
            if not self.settings.USE_MOCK_INGRES:
                raise  # Only raise for production INGRES
    
    async def get_groundwater_level(
        self, 
        district: str, 
        state: Optional[str] = None,
        block: Optional[str] = None,
        season: str = "post_monsoon"
    ) -> Dict[str, Any]:
        """Get groundwater level data for a location"""
        
        if not self.initialized:
            raise RuntimeError("INGRES Service not initialized")
        
        # Create cache key
        cache_key = f"groundwater_level:{district.lower()}:{season}"
        
        # Try cache first
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                logger.info(f"📋 Cache hit for groundwater level: {district}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
        
        # Fetch from API
        try:
            params = {
                "district": district,
                "season": season
            }
            if block:
                params["block"] = block
                
            response = await self.http_client.get("/groundwater/level", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"🌊 Fetched groundwater level data for {district}")
            
            # Cache the response
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.settings.INGRES_CACHE_TTL,
                    json.dumps(data)
                )
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error fetching groundwater level: {str(e)}")
            # Return fallback data
            return self._get_fallback_data("groundwater_level", district)
    
    async def get_water_quality(
        self, 
        district: str, 
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get water quality data for a location"""
        
        if not self.initialized:
            raise RuntimeError("INGRES Service not initialized")
        
        cache_key = f"water_quality:{district.lower()}"
        
        # Try cache first
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                logger.info(f"📋 Cache hit for water quality: {district}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
        
        # Fetch from API
        try:
            params = {"district": district}
            response = await self.http_client.get("/groundwater/quality", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"🧪 Fetched water quality data for {district}")
            
            # Cache the response
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.settings.INGRES_CACHE_TTL,
                    json.dumps(data)
                )
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error fetching water quality: {str(e)}")
            return self._get_fallback_data("water_quality", district)
    
    async def get_rainfall_data(
        self, 
        district: str, 
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get rainfall and recharge data"""
        
        if not self.initialized:
            raise RuntimeError("INGRES Service not initialized")
        
        year = year or datetime.now().year
        cache_key = f"rainfall:{district.lower()}:{year}"
        
        # Try cache first
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                logger.info(f"📋 Cache hit for rainfall data: {district}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
        
        # Fetch from API
        try:
            params = {"district": district, "year": year}
            response = await self.http_client.get("/rainfall", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"🌧️ Fetched rainfall data for {district}")
            
            # Cache the response
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.settings.INGRES_CACHE_TTL,
                    json.dumps(data)
                )
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error fetching rainfall data: {str(e)}")
            return self._get_fallback_data("rainfall", district)
    
    async def get_drilling_recommendation(
        self, 
        district: str, 
        state: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get borewell drilling recommendations"""
        
        if not self.initialized:
            raise RuntimeError("INGRES Service not initialized")
        
        cache_key = f"drilling:{district.lower()}"
        
        # Try cache first
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                logger.info(f"📋 Cache hit for drilling recommendation: {district}")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
        
        # Fetch from API
        try:
            params = {"district": district}
            response = await self.http_client.get("/drilling/recommendation", params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"⚒️ Fetched drilling recommendation for {district}")
            
            # Cache the response
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.settings.INGRES_CACHE_TTL,
                    json.dumps(data)
                )
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Error fetching drilling recommendation: {str(e)}")
            return self._get_fallback_data("drilling", district)
    
    async def get_available_districts(self) -> List[Dict[str, Any]]:
        """Get list of available districts"""
        
        cache_key = "available_districts"
        
        # Try cache first
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                logger.info("📋 Cache hit for available districts")
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"Cache read error: {str(e)}")
        
        # Fetch from API
        try:
            response = await self.http_client.get("/districts")
            response.raise_for_status()
            
            data = response.json()
            districts = data.get("data", [])
            logger.info(f"📍 Fetched {len(districts)} available districts")
            
            # Cache the response for longer (districts don't change often)
            try:
                await self.redis_client.setex(
                    cache_key,
                    86400,  # 24 hours
                    json.dumps(districts)
                )
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return districts
            
        except Exception as e:
            logger.error(f"❌ Error fetching available districts: {str(e)}")
            # Return basic fallback districts
            return [
                {"district": "Nalanda", "state": "Bihar", "geology": "Alluvial"},
                {"district": "Jalgaon", "state": "Maharashtra", "geology": "Deccan Trap"},
                {"district": "Anantapur", "state": "Andhra Pradesh", "geology": "Hard Rock"}
            ]
    
    def _get_fallback_data(self, data_type: str, district: str) -> Dict[str, Any]:
        """Get fallback data when API is unavailable"""
        
        timestamp = datetime.now().isoformat()
        
        fallback_data = {
            "groundwater_level": {
                "status": "success",
                "data": {
                    "district": district.title(),
                    "water_level_mbgl": 12.5,
                    "status": "Moderate",
                    "gec_category": "Semi-Critical",
                    "trend": "stable",
                    "source": "jalBuddy Fallback Data",
                    "note": "Live data temporarily unavailable"
                },
                "timestamp": timestamp
            },
            "water_quality": {
                "status": "success",
                "data": {
                    "district": district.title(),
                    "parameters": {
                        "tds": 650.0,
                        "fluoride": 0.8,
                        "nitrate": 25.0
                    },
                    "potable": True,
                    "recommendation": "Generally safe for consumption",
                    "source": "jalBuddy Fallback Data",
                    "note": "Live data temporarily unavailable"
                },
                "timestamp": timestamp
            },
            "rainfall": {
                "status": "success", 
                "data": {
                    "district": district.title(),
                    "total_rainfall_mm": 750.0,
                    "status": "Normal",
                    "source": "jalBuddy Fallback Data",
                    "note": "Live data temporarily unavailable"
                },
                "timestamp": timestamp
            },
            "drilling": {
                "status": "success",
                "data": {
                    "district": district.title(),
                    "success_probability_percent": 65,
                    "recommended_depth_range": {
                        "minimum_m": 100,
                        "maximum_m": 200
                    },
                    "source": "jalBuddy Fallback Data",
                    "note": "Live data temporarily unavailable"
                },
                "timestamp": timestamp
            }
        }
        
        return fallback_data.get(data_type, {
            "status": "error",
            "message": "Data temporarily unavailable",
            "timestamp": timestamp
        })
    
    async def cleanup(self):
        """Cleanup INGRES service resources"""
        logger.info("🧹 Cleaning up INGRES Service...")
        
        if self.http_client:
            await self.http_client.aclose()
            
        if self.redis_client:
            await self.redis_client.close()
            
        self.initialized = False
        logger.info("✅ INGRES Service cleanup complete")
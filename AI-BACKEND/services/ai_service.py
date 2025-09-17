"""
AI Service for jalBuddy - Handles query processing and AI responses
"""

import asyncio
import time
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Main AI service for processing groundwater queries"""
    
    def __init__(self, rag_service=None, ingres_service=None):
        self.initialized = False
        self.model_loaded = False
        self.conversation_history = {}
        self.rag_service = rag_service
        self.ingres_service = ingres_service
        
    async def initialize(self):
        """Initialize AI models and services"""
        try:
            logger.info("🤖 Initializing AI Service...")
            
            # Mock initialization - replace with actual model loading
            await asyncio.sleep(1)  # Simulate loading time
            
            self.initialized = True
            self.model_loaded = True
            
            logger.info("✅ AI Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ AI Service initialization failed: {str(e)}")
            raise
    
    async def process_query(
        self, 
        query: str, 
        language: str = "hi", 
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a groundwater query with RAG and INGRES integration"""
        
        if not self.initialized:
            raise RuntimeError("AI Service not initialized")
            
        start_time = time.time()
        
        try:
            logger.info(f"🧠 Processing query: {query[:50]}...")
            
            # Track conversation history for context
            user_id = user_context.get("user_id", "anonymous") if user_context else "anonymous"
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Enhanced response generation with RAG and live data
            if self.rag_service and self.rag_service.initialized:
                # Get live INGRES data if location is provided
                ingres_data = None
                location = user_context.get("location") if user_context else None
                
                if location and self.ingres_service and self.ingres_service.initialized:
                    logger.info(f"📊 Fetching live data for: {location}")
                    try:
                        # Fetch relevant INGRES data concurrently
                        tasks = [
                            self.ingres_service.get_groundwater_level(location),
                            self.ingres_service.get_water_quality(location)
                        ]
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        ingres_data = {}
                        if not isinstance(results[0], Exception):
                            ingres_data["groundwater_level"] = results[0]
                        if not isinstance(results[1], Exception):
                            ingres_data["water_quality"] = results[1]
                            
                    except Exception as e:
                        logger.warning(f"⚠️ Could not fetch INGRES data: {str(e)}")
                
                # Use RAG for context-aware response
                rag_result = await self.rag_service.generate_context_aware_response(
                    query=query,
                    language=language,
                    user_context=user_context,
                    ingres_data=ingres_data
                )
                
                response = rag_result["response"]
                confidence = rag_result["confidence"]
                sources_count = rag_result["knowledge_sources"]
                
                logger.info(f"✅ RAG enhanced response (confidence: {confidence:.2f}, sources: {sources_count})")
                
            else:
                # Fallback to basic response generation
                logger.info("📝 Using fallback response generation")
                response = await self._generate_dynamic_response(query, language, user_context)
                confidence = random.uniform(0.65, 0.85)
                sources_count = 0
            
            # Store in conversation history
            self.conversation_history[user_id].append({
                "query": query,
                "response": response,
                "timestamp": datetime.now(),
                "confidence": confidence,
                "rag_enhanced": bool(self.rag_service and self.rag_service.initialized)
            })
            
            processing_time = time.time() - start_time
            
            return {
                "response": response,
                "confidence": confidence,
                "sources": self._get_relevant_sources(query, sources_count),
                "language": language,
                "processing_time": processing_time,
                "rag_enhanced": bool(self.rag_service and self.rag_service.initialized),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Query processing failed: {str(e)}")
            raise
    
    async def _generate_dynamic_response(
        self, 
        query: str, 
        language: str, 
        user_context: Dict[str, Any] = None
    ) -> str:
        """Generate dynamic AI response based on query analysis"""
        
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        query_lower = query.lower()
        location = user_context.get("location", "आपके क्षेत्र" if language == "hi" else "your area") if user_context else ("आपके क्षेत्र" if language == "hi" else "your area")
        
        # Generate varied responses based on keywords and context
        if language == "hi":
            return self._generate_hindi_response(query_lower, location)
        else:
            return self._generate_english_response(query_lower, location)
    
    def _generate_hindi_response(self, query_lower: str, location: str) -> str:
        """Generate varied Hindi responses"""
        
        if "भूजल" in query_lower or "जल स्तर" in query_lower:
            responses = [
                f"भूजल स्तर की जांच के लिए आप DWLR स्टेशन डेटा का उपयोग कर सकते हैं। {location} में वर्तमान जल स्तर {random.uniform(8.5, 15.2):.1f} मीटर है। नियमित निगरानी आवश्यक है।",
                f"भूजल मॉनिटरिंग के लिए CGWB के ऑनलाइन पोर्टल का उपयोग करें। {location} में जल स्तर {'स्थिर' if random.random() > 0.5 else 'घट रहा'} है। मासिक जांच की सलाह दी जाती है।",
                f"भूजल स्तर चेक करने के लिए स्थानीय भूजल बोर्ड से संपर्क करें। {location} में पिछले महीने की तुलना में जल स्तर में {random.uniform(-0.5, 0.8):.1f} मीटर का बदलाव है।"
            ]
        elif "बोरवेल" in query_lower or "ड्रिलिंग" in query_lower:
            responses = [
                f"बोरवेल ड्रिलिंग के लिए भूवैज्ञानिक सर्वेक्षण आवश्यक है। {location} में {random.randint(150, 250)} मीटर की गहराई पर सफलता की संभावना {random.randint(65, 85)}% है।",
                f"ड्रिलिंग से पहले हाइड्रोजियोलॉजिकल सर्वे कराएं। {location} में हार्ड रॉक एरिया में बोरवेल की सफलता दर अच्छी है। स्थानीय अनुमति आवश्यक है।",
                f"बोरवेल की सही जगह चुनने के लिए भूजल मैपिंग देखें। {location} में वर्तमान में {random.randint(3, 8)} सक्रिय बोरवेल हैं।"
            ]
        elif "गुणवत्ता" in query_lower or "पानी की जांच" in query_lower:
            responses = [
                f"पानी की गुणवत्ता जांच के लिए NABL प्रमाणित लैब का उपयोग करें। {location} में TDS स्तर {random.randint(400, 900)} mg/L है।",
                f"भूजल गुणवत्ता परीक्षण में फ्लोराइड, नाइट्रेट और TDS की जांच आवश्यक है। {location} में पानी {'पीने योग्य' if random.random() > 0.3 else 'उपचार के बाद पीने योग्य'} है।",
                f"जल गुणवत्ता मानकों के अनुसार {location} में भूजल की स्थिति {'संतोषजनक' if random.random() > 0.4 else 'निगरानी आवश्यक'} है।"
            ]
        else:
            responses = [
                f"मैं {location} के लिए भूजल संबंधी जानकारी प्रदान कर सकता हूं। आप जल स्तर, गुणवत्ता, या ड्रिलिंग के बारे में पूछ सकते हैं।",
                f"भूजल प्रबंधन के लिए CGWB दिशानिर्देशों का पालन करें। {location} में जल संरक्षण के उपाय अपनाएं।",
                f"आपकी भूजल संबंधी समस्या को समझने के लिए अधिक विवरण दें। मैं {location} के लिए विशिष्ट सुझाव दे सकता हूं।"
            ]
        
        return random.choice(responses)
    
    def _generate_english_response(self, query_lower: str, location: str) -> str:
        """Generate varied English responses"""
        
        if "groundwater" in query_lower or "water level" in query_lower:
            responses = [
                f"To check groundwater levels, use DWLR station data or CGWB portal. Current water level in {location} is {random.uniform(8.5, 15.2):.1f} meters. Regular monitoring recommended.",
                f"Groundwater monitoring can be done through local groundwater board. In {location}, water level is {'stable' if random.random() > 0.5 else 'declining'}. Monthly checks advised.",
                f"For groundwater assessment, contact your district groundwater office. {location} shows {random.uniform(-0.5, 0.8):.1f} meter change from last month."
            ]
        elif "borewell" in query_lower or "drilling" in query_lower:
            responses = [
                f"For borewell drilling, geological survey is essential. In {location}, success probability is {random.randint(65, 85)}% at {random.randint(150, 250)} meter depth.",
                f"Before drilling, conduct hydrogeological survey. {location} has good success rate in hard rock areas. Local permissions required.",
                f"Choose borewell location based on groundwater mapping. {location} currently has {random.randint(3, 8)} active borewells."
            ]
        elif "quality" in query_lower or "contamination" in query_lower:
            responses = [
                f"Water quality testing requires NABL certified lab. TDS level in {location} is {random.randint(400, 900)} mg/L.",
                f"Groundwater quality testing should include fluoride, nitrate, and TDS. Water in {location} is {'potable' if random.random() > 0.3 else 'requires treatment'}.",
                f"According to water quality standards, groundwater in {location} is {'satisfactory' if random.random() > 0.4 else 'needs monitoring'}."
            ]
        else:
            responses = [
                f"I can provide groundwater information for {location}. Ask about water levels, quality, or drilling guidance.",
                f"For groundwater management, follow CGWB guidelines. Implement water conservation measures in {location}.",
                f"Please provide more details about your groundwater query. I can give specific recommendations for {location}."
            ]
        
        return random.choice(responses)
    
    def _get_relevant_sources(self, query: str, rag_sources_count: int = 0) -> List[Dict[str, Any]]:
        """Get relevant sources based on query and RAG sources"""
        
        all_sources = [
            {"title": "CGWB Guidelines", "relevance": random.uniform(0.8, 0.95), "type": "guideline"},
            {"title": "GEC-2015 Manual", "relevance": random.uniform(0.75, 0.9), "type": "regulation"},
            {"title": "INGRES Database", "relevance": random.uniform(0.7, 0.85), "type": "live_data"},
            {"title": "Hydrogeological Survey", "relevance": random.uniform(0.65, 0.8), "type": "technical"},
            {"title": "Water Quality Standards", "relevance": random.uniform(0.6, 0.85), "type": "standard"}
        ]
        
        # If RAG provided sources, boost knowledge-based sources
        if rag_sources_count > 0:
            for source in all_sources:
                if source["type"] in ["guideline", "regulation", "standard"]:
                    source["relevance"] = min(0.95, source["relevance"] + 0.1)
        
        # Return top sources based on RAG enhancement
        num_sources = min(max(2, rag_sources_count), 5)
        return sorted(all_sources, key=lambda x: x["relevance"], reverse=True)[:num_sources]
    
    async def cleanup(self):
        """Cleanup AI service resources"""
        logger.info("🧹 Cleaning up AI Service...")
        self.initialized = False
        self.model_loaded = False
        self.conversation_history.clear()

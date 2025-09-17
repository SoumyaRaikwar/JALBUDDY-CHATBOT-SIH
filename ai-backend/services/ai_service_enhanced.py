"""
Enhanced AI Service with Real LLM Integration
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

from models.llm_manager import LLMManager
from config.settings import get_settings

logger = logging.getLogger(__name__)

class EnhancedAIService:
    """Enhanced AI Service with real intelligence"""

    def __init__(self):
        self.settings = get_settings()
        self.llm_manager = None
        self.is_initialized = False
        self.query_count = 0

    async def initialize(self):
        """Initialize enhanced AI components"""
        try:
            logger.info("🤖 Initializing Enhanced AI Service...")

            # Initialize real LLM manager
            self.llm_manager = LLMManager()
            logger.info("✅ LLM Manager with GPT-4 ready")

            self.is_initialized = True
            logger.info("🎯 Enhanced AI Service operational!")

        except Exception as e:
            logger.error(f"❌ Initialization failed: {str(e)}")
            raise

    async def process_query(self, 
                          query: str, 
                          language: str = "hi",
                          user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process query with real AI"""
        start_time = time.time()

        try:
            self.query_count += 1
            logger.info(f"🔍 Processing query #{self.query_count}: {query[:50]}...")

            # Build context for groundwater expertise
            context = self._build_groundwater_context(query, user_context)

            # Generate response using real LLM
            llm_response = await self.llm_manager.generate_response(
                prompt=query,
                context=context,
                language=language
            )

            processing_time = time.time() - start_time

            result = {
                "response": llm_response.content,
                "confidence": llm_response.confidence,
                "model_used": llm_response.model_used,
                "tokens_used": llm_response.tokens_used,
                "processing_time": processing_time,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "query_id": self.query_count,
                "sources": [{
                    "type": "AI Model",
                    "model": llm_response.model_used,
                    "confidence": llm_response.confidence
                }],
                "response_type": "text"
            }

            logger.info(f"✅ Query processed in {processing_time:.2f}s using {llm_response.model_used}")
            return result

        except Exception as e:
            logger.error(f"❌ Query processing failed: {str(e)}")

            # Fallback response
            fallback_msg = ("मुझे खुशी होगी आपकी सहायता करने में। कृपया अपना प्रश्न दोबारा पूछें।" 
                          if language == "hi" else 
                          "I'd be happy to help. Please try asking again.")

            return {
                "response": fallback_msg,
                "confidence": 0.3,
                "model_used": "fallback",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _build_groundwater_context(self, query: str, user_context: Optional[Dict]) -> str:
        """Build groundwater-specific context"""
        context_parts = [
            "You are jalBuddy, an expert groundwater consultant for India.",
            "Provide practical advice based on GEC-2015 methodology and INGRES data.",
            "Use both Hindi and English technical terms appropriately.",
            "Focus on actionable, safe, and sustainable groundwater practices."
        ]

        if user_context and user_context.get('location'):
            context_parts.append(f"User location: {user_context['location']}")

        return " ".join(context_parts)

    async def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        stats = {
            "status": "operational" if self.is_initialized else "initializing",
            "total_queries": self.query_count,
            "timestamp": datetime.now().isoformat()
        }

        if self.llm_manager:
            stats.update(self.llm_manager.get_stats())

        return stats

    async def cleanup(self):
        """Cleanup resources"""
        logger.info("🧹 Cleaning up Enhanced AI Service...")
        logger.info("✅ Cleanup complete")

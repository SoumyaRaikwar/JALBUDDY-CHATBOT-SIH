"""
RAG (Retrieval Augmented Generation) Service for jalBuddy using ChromaDB
Implements knowledge base search and context-aware response generation
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import hashlib
import os

import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

from config.settings import get_settings

logger = logging.getLogger(__name__)

class ChromaRAGService:
    """RAG service for context-aware groundwater consultations using ChromaDB"""
    
    def __init__(self):
        self.settings = get_settings()
        self.chroma_client: Optional[chromadb.Client] = None
        self.collection = None
        self.embedding_model: Optional[SentenceTransformer] = None
        self.initialized = False
        
        # Collection name for GEC-2015 knowledge base
        self.knowledge_collection = self.settings.VECTOR_COLLECTION
        
        # Ensure data directory exists
        os.makedirs(self.settings.DATA_DIR, exist_ok=True)
        self.chroma_db_path = os.path.join(self.settings.DATA_DIR, "chroma_db")
        
    async def initialize(self):
        """Initialize RAG service with ChromaDB and embedding model"""
        try:
            logger.info("🧠 Initializing ChromaDB RAG Service...")
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_db_path)
            logger.info(f"🔗 Connected to ChromaDB at {self.chroma_db_path}")
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer(self.settings.EMBEDDING_MODEL)
            logger.info(f"🔤 Loaded embedding model: {self.settings.EMBEDDING_MODEL}")
            
            # Create embedding function for ChromaDB
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.settings.EMBEDDING_MODEL
            )
            
            # Get or create knowledge collection
            try:
                self.collection = self.chroma_client.get_collection(
                    name=self.knowledge_collection,
                    embedding_function=embedding_fn
                )
                logger.info(f"📚 Connected to existing collection: {self.knowledge_collection}")
            except (ValueError, Exception):
                # Collection doesn't exist, create it
                self.collection = self.chroma_client.create_collection(
                    name=self.knowledge_collection,
                    embedding_function=embedding_fn
                )
                logger.info(f"📚 Created new collection: {self.knowledge_collection}")
            
            # Load initial GEC-2015 knowledge if collection is empty
            await self._load_initial_knowledge()
            
            self.initialized = True
            logger.info("✅ ChromaDB RAG Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ RAG Service initialization failed: {str(e)}")
            raise
    
    async def _load_initial_knowledge(self):
        """Load initial GEC-2015 knowledge base if collection is empty"""
        try:
            # Check if collection already has documents
            collection_count = self.collection.count()
            
            if collection_count > 0:
                logger.info(f"📚 Knowledge base already loaded ({collection_count} documents)")
                return
            
            logger.info("📚 Loading initial GEC-2015 knowledge base...")
            
            # GEC-2015 knowledge chunks
            knowledge_chunks = [
                {
                    "id": "gec_categories_en",
                    "content": "GEC-2015 classifies groundwater assessment units into four categories: Safe (stage of development <70% and declining trend <0.1m/year), Semi-Critical (70-90% development OR declining trend 0.1-0.5m/year), Critical (90-100% development OR declining trend 0.5-1.0m/year), and Over-Exploited (>100% development OR declining trend >1.0m/year).",
                    "language": "en",
                    "document_type": "gec2015",
                    "section": "classification",
                    "keywords": ["classification", "categories", "safe", "critical", "over-exploited", "semi-critical"]
                },
                {
                    "id": "gec_categories_hi", 
                    "content": "GEC-2015 भूजल मूल्यांकन इकाइयों को चार श्रेणियों में वर्गीकृत करता है: सुरक्षित (विकास का चरण <70% और गिरावट की प्रवृत्ति <0.1मी/वर्ष), अर्ध-महत्वपूर्ण (70-90% विकास या गिरावट 0.1-0.5मी/वर्ष), महत्वपूर्ण (90-100% विकास या गिरावट 0.5-1.0मी/वर्ष), और अति-दोहित (>100% विकास या गिरावट >1.0मी/वर्ष)।",
                    "language": "hi",
                    "document_type": "gec2015",
                    "section": "classification", 
                    "keywords": ["वर्गीकरण", "श्रेणी", "सुरक्षित", "महत्वपूर्ण", "अति-दोहित", "अर्ध-महत्वपूर्ण"]
                },
                {
                    "id": "water_quality_standards_en",
                    "content": "IS 10500:2012 specifies water quality standards: TDS <500mg/L (acceptable <2000mg/L), Fluoride <1.0mg/L (max 1.5mg/L), Nitrate <45mg/L, pH 6.5-8.5, Chloride <250mg/L. For irrigation, TDS up to 3000mg/L may be acceptable depending on crop type and soil conditions.",
                    "language": "en", 
                    "document_type": "standards",
                    "section": "water_quality",
                    "keywords": ["water quality", "standards", "TDS", "fluoride", "nitrate", "pH", "irrigation"]
                },
                {
                    "id": "water_quality_standards_hi",
                    "content": "IS 10500:2012 जल गुणवत्ता मानक निर्दिष्ट करता है: TDS <500mg/L (स्वीकार्य <2000mg/L), फ्लोराइड <1.0mg/L (अधिकतम 1.5mg/L), नाइट्रेट <45mg/L, pH 6.5-8.5, क्लोराइड <250mg/L। सिंचाई के लिए, फसल के प्रकार और मिट्टी की स्थिति के आधार पर 3000mg/L तक TDS स्वीकार्य हो सकता है।",
                    "language": "hi",
                    "document_type": "standards", 
                    "section": "water_quality",
                    "keywords": ["जल गुणवत्ता", "मानक", "TDS", "फ्लोराइड", "नाइट्रेट", "pH", "सिंचाई"]
                },
                {
                    "id": "borewell_guidelines_en",
                    "content": "Borewell construction guidelines: Minimum 100m spacing between borewells, proper casing installation, NOC from State Groundwater Authority required, depth should not exceed twice the static water level, regular water level monitoring mandatory, avoid drilling in over-exploited areas without permission.",
                    "language": "en",
                    "document_type": "guidelines",
                    "section": "borewell_construction",
                    "keywords": ["borewell", "construction", "guidelines", "spacing", "NOC", "depth", "monitoring"]
                },
                {
                    "id": "borewell_guidelines_hi", 
                    "content": "बोरवेल निर्माण दिशानिर्देश: बोरवेल के बीच न्यूनतम 100मी दूरी, उचित केसिंग स्थापना, राज्य भूजल प्राधिकरण से NOC आवश्यक, गहराई स्थिर जल स्तर के दोगुने से अधिक नहीं होनी चाहिए, नियमित जल स्तर निगरानी अनिवार्य, बिना अनुमति अति-दोहित क्षेत्रों में ड्रिलिंग से बचें।",
                    "language": "hi",
                    "document_type": "guidelines",
                    "section": "borewell_construction", 
                    "keywords": ["बोरवेल", "निर्माण", "दिशानिर्देश", "दूरी", "NOC", "गहराई", "निगरानी"]
                },
                {
                    "id": "recharge_methods_en",
                    "content": "Groundwater recharge methods include: Check dams, percolation tanks, recharge wells/shafts, roof-top rainwater harvesting, contour bunding, farm ponds. Effectiveness depends on geology: 15-25% in hard rock areas, 10-20% in alluvial areas. Monsoon recharge contributes 60-80% of annual recharge.",
                    "language": "en",
                    "document_type": "guidelines",
                    "section": "groundwater_recharge",
                    "keywords": ["recharge", "rainwater harvesting", "check dams", "percolation", "monsoon", "effectiveness"]
                },
                {
                    "id": "recharge_methods_hi",
                    "content": "भूजल रिचार्ज के तरीकों में शामिल हैं: चेक डैम, पारगम्यता टैंक, रिचार्ज कुएं/शाफ्ट, छत-टॉप वर्षा जल संचयन, कंटूर बंडिंग, फार्म तालाब। प्रभावशीलता भूविज्ञान पर निर्भर करती है: हार्ड रॉक क्षेत्रों में 15-25%, जलोढ़ क्षेत्रों में 10-20%। मानसून रिचार्ज वार्षिक रिचार्ज का 60-80% योगदान देता है।",
                    "language": "hi", 
                    "document_type": "guidelines",
                    "section": "groundwater_recharge",
                    "keywords": ["रिचार्ज", "वर्षा जल संचयन", "चेक डैम", "पारगम्यता", "मानसून", "प्रभावशीलता"]
                }
            ]
            
            # Prepare data for ChromaDB
            documents = [chunk["content"] for chunk in knowledge_chunks]
            metadatas = []
            ids = []
            
            for chunk in knowledge_chunks:
                ids.append(chunk["id"])
                metadata = {k: v for k, v in chunk.items() if k not in ["id", "content"]}
                # Convert keywords list to string for ChromaDB
                if "keywords" in metadata and isinstance(metadata["keywords"], list):
                    metadata["keywords"] = ",".join(metadata["keywords"])
                metadatas.append(metadata)
            
            # Add documents to ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✅ Loaded {len(knowledge_chunks)} knowledge documents")
            
        except Exception as e:
            logger.error(f"❌ Error loading initial knowledge: {str(e)}")
            # Don't raise - service can still work without initial knowledge
    
    async def search_knowledge(
        self,
        query: str,
        language: str = "en",
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant information"""
        
        if not self.initialized:
            raise RuntimeError("RAG Service not initialized")
        
        try:
            # Search in ChromaDB
            search_results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where={"language": language} if language else None
            )
            
            # Format results
            results = []
            if search_results["documents"] and search_results["documents"][0]:
                documents = search_results["documents"][0]
                metadatas = search_results["metadatas"][0]
                distances = search_results["distances"][0] if "distances" in search_results else [0.5] * len(documents)
                
                for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                    # Convert distance to similarity score (ChromaDB uses distance, lower is better)
                    similarity = 1.0 - distance
                    
                    if similarity >= score_threshold:
                        result = {
                            "content": doc,
                            "score": similarity,
                            "language": metadata.get("language", "en"),
                            "section": metadata.get("section", "general"),
                            "document_type": metadata.get("document_type", "unknown"),
                            "keywords": metadata.get("keywords", "").split(",") if metadata.get("keywords") else []
                        }
                        results.append(result)
            
            logger.info(f"🔍 Found {len(results)} relevant knowledge chunks for query")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching knowledge base: {str(e)}")
            return []
    
    async def generate_context_aware_response(
        self,
        query: str,
        language: str = "en",
        user_context: Optional[Dict[str, Any]] = None,
        ingres_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate context-aware response using RAG"""
        
        try:
            # Search relevant knowledge
            knowledge_chunks = await self.search_knowledge(
                query=query,
                language=language,
                limit=self.settings.TOP_K_RESULTS,
                score_threshold=self.settings.SIMILARITY_THRESHOLD
            )
            
            # Build context from knowledge and live data
            context_parts = []
            
            # Add relevant knowledge
            if knowledge_chunks:
                context_parts.append("Relevant Guidelines:")
                for chunk in knowledge_chunks[:3]:  # Top 3 most relevant
                    context_parts.append(f"- {chunk['content']}")
            
            # Add live INGRES data if available
            if ingres_data:
                context_parts.append("\nCurrent Data:")
                if "groundwater_level" in ingres_data:
                    level_data = ingres_data["groundwater_level"].get("data", {})
                    if level_data:
                        context_parts.append(f"- Water level: {level_data.get('water_level_mbgl', 'N/A')} meters")
                        context_parts.append(f"- Status: {level_data.get('status', 'N/A')}")
                        context_parts.append(f"- Category: {level_data.get('gec_category', 'N/A')}")
                
                if "water_quality" in ingres_data:
                    quality_data = ingres_data["water_quality"].get("data", {})
                    if quality_data and "parameters" in quality_data:
                        params = quality_data["parameters"]
                        context_parts.append(f"- TDS: {params.get('tds', 'N/A')} mg/L")
                        context_parts.append(f"- Fluoride: {params.get('fluoride', 'N/A')} mg/L")
            
            # Generate contextual response
            response = await self._generate_response_with_context(
                query=query,
                context="\n".join(context_parts),
                language=language,
                user_context=user_context
            )
            
            return {
                "response": response,
                "knowledge_sources": len(knowledge_chunks),
                "context_used": bool(context_parts),
                "confidence": min(0.95, 0.7 + (len(knowledge_chunks) * 0.05)),
                "language": language
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating context-aware response: {str(e)}")
            # Return fallback response
            return {
                "response": self._get_fallback_response(query, language),
                "knowledge_sources": 0,
                "context_used": False,
                "confidence": 0.5,
                "language": language
            }
    
    async def _generate_response_with_context(
        self,
        query: str,
        context: str,
        language: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate response using context (simplified - would use LLM in production)"""
        
        # Extract location from user context
        location = "your area"
        if user_context:
            location = user_context.get("location", location)
        
        # Simple template-based response generation
        # In production, this would use a fine-tuned LLM
        query_lower = query.lower()
        
        if language == "hi":
            return self._generate_hindi_contextual_response(query_lower, context, location)
        else:
            return self._generate_english_contextual_response(query_lower, context, location)
    
    def _generate_english_contextual_response(self, query: str, context: str, location: str) -> str:
        """Generate English response with context"""
        
        if "category" in query or "classification" in query or "gec" in query:
            return f"Based on GEC-2015 guidelines and current data for {location}: {context[:200]}... The classification helps determine appropriate management strategies for sustainable groundwater use."
        
        elif "quality" in query or "safe" in query or "drink" in query:
            return f"Water quality assessment for {location}: {context[:200]}... Regular testing is recommended to ensure safety for intended use."
        
        elif "borewell" in query or "drilling" in query or "bore" in query:
            return f"For borewell construction in {location}: {context[:200]}... Please ensure compliance with local regulations and spacing requirements."
        
        elif "recharge" in query or "rainwater" in query:
            return f"Groundwater recharge methods for {location}: {context[:200]}... Implementation depends on local geological and climatic conditions."
        
        else:
            return f"Based on available guidelines and data for {location}: {context[:300]}... For specific recommendations, please provide more details about your requirements."
    
    def _generate_hindi_contextual_response(self, query: str, context: str, location: str) -> str:
        """Generate Hindi response with context"""
        
        if "श्रेणी" in query or "वर्गीकरण" in query or "gec" in query:
            return f"GEC-2015 दिशानिर्देशों और {location} के वर्तमान डेटा के आधार पर: {context[:200]}... वर्गीकरण टिकाऊ भूजल उपयोग के लिए उपयुक्त प्रबंधन रणनीतियों को निर्धारित करने में मदद करता है।"
        
        elif "गुणवत्ता" in query or "सुरक्षित" in query or "पीने" in query:
            return f"{location} के लिए जल गुणवत्ता मूल्यांकन: {context[:200]}... उद्देश्य के अनुसार सुरक्षा सुनिश्चित करने के लिए नियमित परीक्षण की सलाह दी जाती है।"
        
        elif "बोरवेल" in query or "ड्रिलिंग" in query or "खुदाई" in query:
            return f"{location} में बोरवेल निर्माण के लिए: {context[:200]}... कृपया स्थानीय नियमों और दूरी की आवश्यकताओं का अनुपालन सुनिश्चित करें।"
        
        elif "रिचार्ज" in query or "वर्षा जल" in query:
            return f"{location} के लिए भूजल रिचार्ज के तरीके: {context[:200]}... कार्यान्वयन स्थानीय भूवैज्ञानिक और जलवायु स्थितियों पर निर्भर करता है।"
        
        else:
            return f"{location} के लिए उपलब्ध दिशानिर्देशों और डेटा के आधार पर: {context[:300]}... विशिष्ट सिफारिशों के लिए, कृपया अपनी आवश्यकताओं के बारे में अधिक विवरण प्रदान करें।"
    
    def _get_fallback_response(self, query: str, language: str) -> str:
        """Get fallback response when RAG fails"""
        
        if language == "hi":
            return "मैं आपकी भूजल संबंधी समस्या को समझने में मदद कर सकता हूं। कृपया अपने क्षेत्र और विशिष्ट आवश्यकता के बारे में बताएं।"
        else:
            return "I can help you with groundwater-related queries. Please provide more details about your location and specific requirements."
    
    async def add_knowledge_document(
        self,
        content: str,
        document_type: str,
        language: str = "en",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add a new document to the knowledge base"""
        
        if not self.initialized:
            raise RuntimeError("RAG Service not initialized")
        
        try:
            # Generate unique ID
            doc_id = hashlib.sha256(content.encode()).hexdigest()[:16]
            
            # Prepare metadata
            final_metadata = {
                "document_type": document_type,
                "language": language,
                "added_at": datetime.now().isoformat(),
                **(metadata or {})
            }
            
            # Convert lists to strings for ChromaDB
            for key, value in final_metadata.items():
                if isinstance(value, list):
                    final_metadata[key] = ",".join(str(v) for v in value)
            
            # Add to ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[final_metadata],
                ids=[doc_id]
            )
            
            logger.info(f"📚 Added knowledge document: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Error adding knowledge document: {str(e)}")
            raise
    
    async def cleanup(self):
        """Cleanup RAG service resources"""
        logger.info("🧹 Cleaning up ChromaDB RAG Service...")
        
        # ChromaDB client doesn't need explicit cleanup
        self.initialized = False
        logger.info("✅ ChromaDB RAG Service cleanup complete")
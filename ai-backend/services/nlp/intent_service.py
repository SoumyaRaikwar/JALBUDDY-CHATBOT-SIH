"""
NLP Intent/Entity Service (stub)
This will later use sentence-transformers and optional spaCy/transformers NER.
"""
from typing import Dict, Any

class IntentService:
    def classify_intent(self, text: str, language: str = "hi") -> Dict[str, Any]:
        t = text.lower()
        if any(k in t for k in ["groundwater", "भूजल", "water level", "जल स्तर"]):
            return {"intent": "groundwater_level", "confidence": 0.8}
        if any(k in t for k in ["borewell", "बोरवेल", "drill", "बोरिंग"]):
            return {"intent": "drilling_advice", "confidence": 0.75}
        if any(k in t for k in ["quality", "गुणवत्ता", "tds", "fluoride"]):
            return {"intent": "water_quality", "confidence": 0.7}
        return {"intent": "general_query", "confidence": 0.5}

    def extract_entities(self, text: str, language: str = "hi") -> Dict[str, Any]:
        entities: Dict[str, Any] = {}
        for loc in ["nalanda", "jalgaon", "anantapur"]:
            if loc in text.lower():
                entities["district"] = loc
        return entities


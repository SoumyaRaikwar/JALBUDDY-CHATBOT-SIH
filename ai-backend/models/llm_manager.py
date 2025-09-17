"""
LLM Manager with Real AI Integration
"""

import logging
import time
import asyncio
from typing import List, Optional
from dataclasses import dataclass

# AI imports
try:
    import openai
except ImportError:
    openai = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from config.settings import get_settings

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    content: str
    model_used: str
    tokens_used: int
    response_time: float
    confidence: float

class LLMManager:
    """Manager for multiple LLM providers"""

    def __init__(self):
        self.settings = get_settings()
        self.openai_client = None
        self.anthropic_client = None

        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize available AI clients"""
        try:
            if self.settings.OPENAI_API_KEY and openai:
                self.openai_client = openai.AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
                logger.info("✅ OpenAI client initialized")

            if self.settings.ANTHROPIC_API_KEY and Anthropic:
                self.anthropic_client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
                logger.info("✅ Anthropic client initialized")

        except Exception as e:
            logger.warning(f"AI client initialization warning: {str(e)}")

    async def generate_response(self, prompt: str, context: str = "", language: str = "hi", **kwargs) -> LLMResponse:
        """Generate response using available LLM"""
        start_time = time.time()

        # Try OpenAI first
        if self.openai_client:
            try:
                return await self._generate_openai_response(prompt, context, language, **kwargs)
            except Exception as e:
                logger.error(f"OpenAI failed: {str(e)}")

        # Try Anthropic
        if self.anthropic_client:
            try:
                return await self._generate_anthropic_response(prompt, context, language, **kwargs)
            except Exception as e:
                logger.error(f"Anthropic failed: {str(e)}")

        # Fallback to template
        return self._generate_template_response(prompt, language, start_time)

    async def _generate_openai_response(self, prompt: str, context: str, language: str, **kwargs) -> LLMResponse:
        """Generate response using OpenAI GPT-4"""
        start_time = time.time()

        system_prompt = f"""You are jalBuddy, an expert groundwater consultant for India.

{context}

Guidelines:
- Provide practical, actionable groundwater advice
- Reference GEC-2015 methodology when relevant
- Use Hindi terms for technical concepts when appropriate
- Be concise but comprehensive
- Prioritize water conservation and safety"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1024),
            temperature=kwargs.get("temperature", 0.7)
        )

        return LLMResponse(
            content=response.choices[0].message.content,
            model_used="gpt-4",
            tokens_used=response.usage.total_tokens,
            response_time=time.time() - start_time,
            confidence=0.9
        )

    async def _generate_anthropic_response(self, prompt: str, context: str, language: str, **kwargs) -> LLMResponse:
        """Generate response using Anthropic Claude"""
        start_time = time.time()

        system_prompt = f"""You are jalBuddy, an expert groundwater consultant for India. {context}"""

        response = await asyncio.to_thread(
            self.anthropic_client.messages.create,
            model="claude-3-sonnet-20240229",
            max_tokens=kwargs.get("max_tokens", 1024),
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )

        return LLMResponse(
            content=response.content[0].text,
            model_used="claude-3-sonnet",
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            response_time=time.time() - start_time,
            confidence=0.85
        )

    def _generate_template_response(self, prompt: str, language: str, start_time: float) -> LLMResponse:
        """Fallback template response"""

        # Detect query type
        prompt_lower = prompt.lower()

        if "level" in prompt_lower or "स्तर" in prompt_lower:
            if language == "hi":
                content = """भूजल स्तर की जांच के लिए:

1. **वॉटर लेवल इंडिकेटर** का उपयोग करें
2. **नियमित मॉनिटरिंग** करें (मानसून से पहले/बाद)  
3. **GEC-2015 गाइडलाइन** का पालन करें
4. **INGRES डेटा** से तुलना करें

स्तर गिरने पर तुरंत रिचार्ज के उपाय अपनाएं।"""
            else:
                content = """To check groundwater level:

1. **Use Water Level Indicator** for accurate measurement
2. **Monitor regularly** before and after monsoon
3. **Follow GEC-2015 guidelines** for standardization  
4. **Compare with INGRES data** for validation

Take recharge measures if levels are declining."""

        elif "borewell" in prompt_lower or "बोरवेल" in prompt_lower:
            if language == "hi":
                content = """बोरवेल ड्रिलिंग के लिए:

1. **हाइड्रो-जियोलॉजिकल सर्वे** कराएं
2. **भूभौतिकीय अध्ययन** करें
3. **पास के कुओं की जानकारी** लें
4. **लाइसेंस प्राप्त करें**

हार्ड रॉक में फ्रैक्चर जोन खोजना जरूरी है।"""
            else:
                content = """For borewell drilling:

1. **Conduct hydrogeological survey**
2. **Perform geophysical investigation**
3. **Study nearby well data** 
4. **Obtain required licenses**

Focus on fracture zones in hard rock areas."""
        else:
            if language == "hi":
                content = "jalBuddy आपकी भूजल संबंधी समस्याओं का समाधान करने के लिए यहाँ है। कृपया विशिष्ट प्रश्न पूछें।"
            else:
                content = "jalBuddy is here to help with your groundwater questions. Please ask specific questions."

        return LLMResponse(
            content=content,
            model_used="template_fallback",
            tokens_used=len(content.split()),
            response_time=time.time() - start_time,
            confidence=0.6
        )

    def get_stats(self) -> dict:
        """Get LLM statistics"""
        return {
            "openai_available": bool(self.openai_client),
            "anthropic_available": bool(self.anthropic_client),
            "fallback_available": True
        }

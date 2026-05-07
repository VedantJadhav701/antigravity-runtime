import httpx
import json
import logging
from typing import Optional, Dict, Any
from runtime.intelligence.schemas import IntelligenceProvider, LLMResponse

logger = logging.getLogger("runtime.intelligence.ollama")

class OllamaProvider(IntelligenceProvider):
    """
    Ollama implementation for local LLM inference.
    Default port: 11434
    """
    def __init__(self, model: str = "qwen2.5-coder:3b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    async def complete(self, prompt: str, system_message: Optional[str] = None) -> LLMResponse:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_message,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return LLMResponse(
                content=data["response"],
                model=self.model,
                usage={"total_duration": data.get("total_duration", 0)}
            )

    async def extract_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Specialized method for JSON extraction. 
        Forces the model to return valid JSON.
        """
        system_prompt = f"You are a structured data extractor. Return ONLY valid JSON matching this schema: {json.dumps(schema)}"
        response = await self.complete(prompt, system_message=system_prompt)
        
        try:
            # Basic cleanup of markdown blocks
            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to parse JSON from Ollama: {e}")
            raise ValueError(f"Semantic Failure: Could not extract valid JSON from LLM response.")

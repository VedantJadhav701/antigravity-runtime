from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class LLMResponse(BaseModel):
    content: str
    raw_json: Optional[Dict[str, Any]] = None
    usage: Dict[str, int] = Field(default_factory=dict)
    model: str

class IntelligenceProvider(ABC):
    """
    Abstract interface for local LLM providers.
    """
    @abstractmethod
    async def complete(self, prompt: str, system_message: Optional[str] = None) -> LLMResponse:
        pass

    @abstractmethod
    async def extract_json(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        pass

class DraftTaskSpec(BaseModel):
    """
    The probabilistic output from the Intent Engine.
    Needs to be validated by the Kernel.
    """
    project_type: str
    template_id: str
    features: List[str] = Field(default_factory=list)
    reasoning: str

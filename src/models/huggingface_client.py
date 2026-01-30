"""
HuggingFace Client Module
Provides interface to HuggingFace models for text generation.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import asyncio
from loguru import logger


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    repetition_penalty: float = 1.1


class HuggingFaceClient:
    """
    Client for interacting with HuggingFace models.
    Supports both API inference and local models.
    """
    
    def __init__(
        self,
        api_key: str,
        default_model: str = "mistralai/Mistral-7B-Instruct-v0.2",
        use_api: bool = True
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.use_api = use_api
        self.api_url = "https://api-inference.huggingface.co/models"
        self._client = None
        self._local_model = None
        
    async def initialize(self):
        """Initialize the client."""
        if self.use_api:
            await self._init_api_client()
        else:
            await self._init_local_model()
    
    async def _init_api_client(self):
        """Initialize API client."""
        try:
            import aiohttp
            self._client = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            logger.info("HuggingFace API client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize API client: {e}")
    
    async def _init_local_model(self):
        """Initialize local model using transformers."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            logger.info(f"Loading model: {self.default_model}")
            
            self._tokenizer = AutoTokenizer.from_pretrained(self.default_model)
            self._local_model = AutoModelForCausalLM.from_pretrained(
                self.default_model,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            logger.info("Local model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load local model: {e}")
            self.use_api = True
            await self._init_api_client()
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> str:
        """Generate text from prompt."""
        model = model or self.default_model
        config = config or GenerationConfig()
        
        if self.use_api:
            return await self._generate_api(prompt, model, config)
        else:
            return await self._generate_local(prompt, config)
    
    async def _generate_api(
        self,
        prompt: str,
        model: str,
        config: GenerationConfig
    ) -> str:
        """Generate text using HuggingFace API."""
        if not self._client:
            await self._init_api_client()
        
        url = f"{self.api_url}/{model}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": config.max_new_tokens,
                "temperature": config.temperature,
                "top_p": config.top_p,
                "top_k": config.top_k,
                "do_sample": config.do_sample,
                "repetition_penalty": config.repetition_penalty
            }
        }
        
        try:
            async with self._client.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated = result[0].get("generated_text", "")
                        # Remove the original prompt from response
                        if generated.startswith(prompt):
                            generated = generated[len(prompt):].strip()
                        return generated
                    
                    return str(result)
                else:
                    error = await response.text()
                    logger.error(f"API error: {error}")
                    return ""
                    
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return ""
    
    async def _generate_local(
        self,
        prompt: str,
        config: GenerationConfig
    ) -> str:
        """Generate text using local model."""
        if not self._local_model:
            logger.error("Local model not initialized")
            return ""
        
        try:
            inputs = self._tokenizer(prompt, return_tensors="pt")
            inputs = inputs.to(self._local_model.device)
            
            outputs = self._local_model.generate(
                **inputs,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                do_sample=config.do_sample,
                repetition_penalty=config.repetition_penalty,
                pad_token_id=self._tokenizer.eos_token_id
            )
            
            generated = self._tokenizer.decode(
                outputs[0][inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )
            
            return generated.strip()
            
        except Exception as e:
            logger.error(f"Local generation error: {e}")
            return ""
    
    async def embed_text(
        self,
        text: str,
        model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ) -> List[float]:
        """Generate text embeddings."""
        if self.use_api:
            return await self._embed_api(text, model)
        else:
            return await self._embed_local(text, model)
    
    async def _embed_api(self, text: str, model: str) -> List[float]:
        """Generate embeddings using API."""
        if not self._client:
            await self._init_api_client()
        
        url = f"{self.api_url}/{model}"
        
        try:
            async with self._client.post(url, json={"inputs": text}) as response:
                if response.status == 200:
                    result = await response.json()
                    return result if isinstance(result, list) else []
                return []
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return []
    
    async def _embed_local(self, text: str, model: str) -> List[float]:
        """Generate embeddings using local model."""
        try:
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer(model)
            embedding = model.encode(text)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Local embedding error: {e}")
            return []
    
    async def classify(
        self,
        text: str,
        labels: List[str],
        model: str = "facebook/bart-large-mnli"
    ) -> Dict[str, float]:
        """Zero-shot classification."""
        if not self._client:
            await self._init_api_client()
        
        url = f"{self.api_url}/{model}"
        
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": labels}
        }
        
        try:
            async with self._client.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return dict(zip(result["labels"], result["scores"]))
                return {}
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {}
    
    async def close(self):
        """Close the client session."""
        if self._client:
            await self._client.close()
            self._client = None

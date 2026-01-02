# app/llm/service.py
import logging
import json
from typing import Dict, List, Optional, Union
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import Config

# Set up logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM providers."""
    
    def __init__(self):
        """Initialize the LLM service based on configuration."""
        self.provider = Config.LLM_PROVIDER
        
        if self.provider == "openai":
            import openai
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = Config.OPENAI_MODEL
        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.ANTHROPIC_MODEL
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
        
        logger.info(f"Initialized LLM service with provider: {self.provider}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_recipe(self, 
                        ingredients: List[str], 
                        dietary_restrictions: Optional[List[str]] = None,
                        cuisine_preference: Optional[str] = None,
                        meal_type: Optional[str] = None) -> str:
        """
        Generate a recipe based on given ingredients and preferences.
        
        Args:
            ingredients: List of available ingredients
            dietary_restrictions: Optional list of dietary restrictions
            cuisine_preference: Optional cuisine preference
            meal_type: Optional meal type (breakfast, lunch, dinner, etc.)
            
        Returns:
            The generated recipe as text
        """
        # Construct prompt from ingredients and preferences
        prompt = self._construct_prompt(
            ingredients, 
            dietary_restrictions, 
            cuisine_preference,
            meal_type
        )
        
        # Log the prompt (for monitoring)
        logger.info(f"Generating recipe with {len(ingredients)} ingredients")
        logger.debug(f"Prompt: {prompt}")
        
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt)
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            raise
    
    def _construct_prompt(self, 
                          ingredients: List[str],
                          dietary_restrictions: Optional[List[str]] = None,
                          cuisine_preference: Optional[str] = None,
                          meal_type: Optional[str] = None) -> str:
        """Construct a prompt for recipe generation."""
        from app.llm.prompts import RECIPE_PROMPT_TEMPLATE
        
        # Format ingredients as a comma-separated list
        ingredients_str = ", ".join(ingredients)
        
        # Format dietary restrictions if provided
        restrictions_str = ""
        if dietary_restrictions and len(dietary_restrictions) > 0:
            restrictions_str = ", ".join(dietary_restrictions)
        
        # Format cuisine preference if provided
        cuisine_str = cuisine_preference if cuisine_preference else ""
        
        # Format meal type if provided
        meal_str = meal_type if meal_type else ""
        
        # Fill the template
        prompt = RECIPE_PROMPT_TEMPLATE.format(
            ingredients=ingredients_str,
            dietary_restrictions=restrictions_str,
            cuisine=cuisine_str,
            meal_type=meal_str
        )
        
        return prompt
    
    def _generate_openai(self, prompt: str) -> str:
        """Generate text using OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant that creates recipes based on available ingredients."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Log token usage for monitoring
        logger.info(f"OpenAI tokens: {response.usage.total_tokens}")
        
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str) -> str:
        """Generate text using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            system="You are a helpful cooking assistant that creates recipes based on available ingredients.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        

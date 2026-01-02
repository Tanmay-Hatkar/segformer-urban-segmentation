# app/llm/parser.py
import re
from typing import Dict, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

class RecipeParser:
    """Parse and structure recipe responses from LLMs."""
    
    def parse_recipe(self, recipe_text: str) -> Dict[str, Any]:
        """
        Parse raw recipe text into structured format.
        
        Args:
            recipe_text: Raw recipe text from LLM
            
        Returns:
            Structured recipe dictionary
        """
        try:
            # Initialize recipe structure
            recipe = {
                "name": "",
                "ingredients": [],
                "instructions": [],
                "cooking_time": "",
                "servings": "",
                "notes": ""
            }
            
            # Extract recipe name (usually the first line)
            lines = recipe_text.strip().split('\n')
            recipe["name"] = lines[0].strip('#* ')
            
            # Extract sections
            current_section = None
            section_content = []
            
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                    
                # Check for section headers
                lower_line = line.lower()
                if "ingredient" in lower_line and (":" in line or line.endswith("s")):
                    if current_section and section_content:
                        self._add_section_to_recipe(recipe, current_section, section_content)
                    current_section = "ingredients"
                    section_content = []
                    continue
                    
                elif any(x in lower_line for x in ["instruction", "direction", "steps", "method"]):
                    if current_section and section_content:
                        self._add_section_to_recipe(recipe, current_section, section_content)
                    current_section = "instructions"
                    section_content = []
                    continue
                    
                elif "time" in lower_line or "cook" in lower_line and ":" in line:
                    if current_section and section_content:
                        self._add_section_to_recipe(recipe, current_section, section_content)
                    current_section = "cooking_time"
                    recipe["cooking_time"] = line.split(":", 1)[1].strip() if ":" in line else line
                    current_section = None
                    section_content = []
                    continue
                    
                elif "serving" in lower_line and ":" in line:
                    if current_section and section_content:
                        self._add_section_to_recipe(recipe, current_section, section_content)
                    current_section = "servings"
                    recipe["servings"] = line.split(":", 1)[1].strip() if ":" in line else line
                    current_section = None
                    section_content = []
                    continue
                    
                elif "note" in lower_line or "tip" in lower_line:
                    if current_section and section_content:
                        self._add_section_to_recipe(recipe, current_section, section_content)
                    current_section = "notes"
                    section_content = []
                    continue
                
                # Add line to current section
                if current_section:
                    section_content.append(line)
            
            # Add the last section
            if current_section and section_content:
                self._add_section_to_recipe(recipe, current_section, section_content)
            
            logger.info(f"Successfully parsed recipe: {recipe['name']}")
            return recipe
            
        except Exception as e:
            logger.error(f"Error parsing recipe: {str(e)}")
            # Return the raw text if parsing fails
            return {
                "name": "Untitled Recipe",
                "raw_text": recipe_text,
                "error": str(e)
            }
    
    def _add_section_to_recipe(self, recipe: Dict[str, Any], section: str, content: list):
        """Add parsed section content to the recipe dict."""
        if section == "ingredients" or section == "instructions":
            # Clean up items (remove numbering, bullets, etc.)
            cleaned_items = []
            for item in content:
                # Remove numbering and bullets
                cleaned = re.sub(r'^\d+[\.\)]?\s*', '', item)
                cleaned = re.sub(r'^[-•*]\s*', '', cleaned)
                cleaned_items.append(cleaned.strip())
            recipe[section] = cleaned_items
        else:
            # For other sections, join as text
            recipe[section] = '\n'.join(content)
# test_llm.py
import os
import sys
import env_vars

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.llm.service import LLMService
from app.llm.parser import RecipeParser

def test_recipe_generation():
    """Simple test to verify LLM service and recipe parser."""
    # Initialize services
    llm_service = LLMService()
    parser = RecipeParser()
    
    # Sample ingredients
    ingredients = ["chicken breast", "rice", "bell pepper", "onion", "garlic"]
    dietary_restrictions = ["no dairy"]
    
    # Generate recipe
    recipe_text = llm_service.generate_recipe(
        ingredients=ingredients,
        dietary_restrictions=dietary_restrictions,
        cuisine_preference="Asian"
    )
    
    print("\n=== RAW RECIPE TEXT ===")
    print(recipe_text)
    
    # Parse recipe
    recipe = parser.parse_recipe(recipe_text)
    
    print("\n=== PARSED RECIPE ===")
    print(f"Name: {recipe['name']}")
    print("\nIngredients:")
    for item in recipe['ingredients']:
        print(f"- {item}")
    
    print("\nInstructions:")
    for i, step in enumerate(recipe['instructions'], 1):
        print(f"{i}. {step}")
    
    print(f"\nCooking Time: {recipe['cooking_time']}")
    print(f"Servings: {recipe['servings']}")
    print(f"Notes: {recipe['notes']}")

if __name__ == "__main__":
    test_recipe_generation()
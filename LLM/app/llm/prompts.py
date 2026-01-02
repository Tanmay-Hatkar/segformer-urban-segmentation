# app/llm/prompts.py

# Basic recipe generation prompt template
RECIPE_PROMPT_TEMPLATE = """
Create a recipe using the following ingredients: {ingredients}.

{dietary_restrictions and "Please respect these dietary restrictions: " + dietary_restrictions + "." or ""}
{cuisine and "I prefer " + cuisine + " cuisine." or ""}
{meal_type and "This should be for " + meal_type + "." or ""}

Please format the recipe with the following sections:
1. Recipe Name
2. Ingredients (with measurements)
3. Instructions (step by step)
4. Cooking Time
5. Servings
6. Notes (including any ingredient substitutions if needed)
"""

# System prompt for recipe generation
RECIPE_SYSTEM_PROMPT = """
You are a professional chef specialized in creating recipes from available ingredients. 
Your recommendations should be practical, delicious, and follow these guidelines:

1. Only use the ingredients provided, or suggest common substitutes
2. Respect any dietary restrictions mentioned
3. Format recipes clearly with sections for ingredients, instructions, cooking time, and servings
4. Include helpful cooking tips where appropriate
5. Focus on achievable recipes for home cooks
"""
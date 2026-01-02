import os

# from dotenv import load_dotenv
# # Load environment variables
# load_dotenv()

# With:
try:
    import env_vars
except ImportError:
    pass  # Continue if file doesn't exist

class Config:
    # LLM settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Default to OpenAI, but can be switched to "anthropic"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # Model settings
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # App settings
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
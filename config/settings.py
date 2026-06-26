import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings:
  # AgDataBox
  AGBOX_API_URL: str = os.getenv("AGBOX_API_URL", "https://adb.md.utfpr.edu.br/api/data/v2/")
  AGBOX_API_KEY: str = os.getenv("AGBOX_API_KEY", "")
  
  # Algoritmo
  MIN_ZONE_WIDTH: float = float(os.getenv("MIN_ZONE_WIDTH", "5.0"))
  MAX_ZONES: int = int(os.getenv("MAX_ZONES", "10"))
  DEFAULT_PESO_GEOMETRICO: float = float(os.getenv("DEFAULT_PESO_GEOMETRICO", "0.3"))
  
  # Geospatial
  DEFAULT_EPSG: int = int(os.getenv("DEFAULT_EPSG", "31983"))
  
  # API
  API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
  API_PORT: int = int(os.getenv("API_PORT", "8000"))
  DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
  
  # Logging
  LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
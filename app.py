from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from config.settings import settings
from interfaces.routes.api_routes import router

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Zoneamento Agrícola com Restrições Geométricas",
    description="""
    API para delineamento de zonas de manejo com restrições operacionais
    
    ## Funcionalidades
    
    * Zoneamento com restrições geométricas (largura de trabalho)
    * Otimização automática do número de zonas
    * Integração com AgDataBox
    * Métricas de avaliação
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "API de Zoneamento Agrícola",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
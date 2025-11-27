from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.chat_handler import ChatHandler

# Initialize FastAPI app
app = FastAPI(
    title="Terminaciones Chat API",
    description="API de chat especializado en terminaciones arquitectónicas (enchapes, pinturas, baños, pisos, acabados)",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat handler (singleton)
chat_handler: Optional[ChatHandler] = None


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    generate_image: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "message": "¿Qué enchape recomiendas para un baño moderno?",
                "generate_image": False,
            }
        }


class ChatResponse(BaseModel):
    response: str
    on_topic: bool
    image_path: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Para un baño moderno, te recomiendo considerar porcelain bathroom tile en tonos white, beige, que tiene un precio de $25-45/m2. Otra excelente alternativa es glass mosaic tiles disponible en multicolor y white, que también funciona muy bien para este tipo de aplicación. Ambas opciones ofrecen buena durabilidad y acabados de calidad.",
                "on_topic": True,
                "image_path": None,
            }
        }


class HealthResponse(BaseModel):
    status: str
    message: str


# Endpoints
@app.on_event("startup")
async def startup_event():
    global chat_handler
    print("Starting Terminaciones Chat API...")
    chat_handler = ChatHandler()
    print("API ready!")


@app.get("/", response_model=Dict)
async def root():
    return {
        "name": "Terminaciones Chat API",
        "version": "1.0.0",
        "description": "API especializada en terminaciones arquitectónicas",
        "endpoints": {
            "POST /chat": "Enviar mensaje al chat",
            "GET /health": "Verificar estado del servicio",
            "GET /materials/catalog": "Obtener catálogo completo de materiales",
            "GET /materials/{category}": "Obtener materiales por categoría",
        },
        "categories": [
            "bathroom_finishes",
            "paints",
            "flooring"
        ]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    if chat_handler is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    return {
        "status": "healthy",
        "message": "Terminaciones Chat API está funcionando correctamente",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if chat_handler is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    try:
        result = chat_handler.process_message(
            message=request.message, generate_image=request.generate_image
        )

        return ChatResponse(
            response=result["response"],
            on_topic=result["on_topic"],
            image_path=result.get("image_path", None),
        )

    except Exception as e:
        print(f"Error processing chat message: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el mensaje: {str(e)}"
        )


@app.get("/materials/catalog")
async def get_materials_catalog():
    if chat_handler is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    try:
        catalog = chat_handler.get_materials_catalog()
        return catalog
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener el catálogo: {str(e)}"
        )


@app.get("/materials/{category}")
async def get_materials_by_category(category: str):
    if chat_handler is None:
        raise HTTPException(status_code=503, detail="Service not initialized")

    valid_categories = ["bathroom_finishes", "paints", "flooring"]

    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Categoría inválida. Categorías válidas: {', '.join(valid_categories)}",
        )

    try:
        materials = chat_handler.get_materials_by_category(category)
        return {"category": category, "materials": materials}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener materiales: {str(e)}"
        )


# Run with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

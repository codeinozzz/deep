# AI Cladding & Facade Designer

AI-powered architectural cladding and facade design assistant that generates technical specifications and photorealistic visualizations using deep learning models.

## Tabla de Contenidos
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [How to Run](#how-to-run)
  - [Option 1: CLI](#option-1-cli-línea-de-comandos---recomendado)
  - [Option 2: Ejemplos Programáticos](#option-2-ejemplos-programáticos)
  - [Option 3: Integración Python](#option-3-integración-en-tu-código-python)
- [API REST Chat](#api-de-chat-para-terminaciones-arquitectónicas)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Architecture](#application-design--architecture)
- [Performance](#performance-notes)
- [Troubleshooting](#troubleshooting)

## Overview

Sistema de diseño arquitectónico con IA que genera:
- **Especificaciones Técnicas**: Usando FLAN-T5-base (250M parámetros)
- **Renders Fotorrealistas**: Usando Stable Diffusion v1.5
- **Chat Especializado**: API REST para consultas sobre terminaciones

**Características:**
- 100% gratuito - sin APIs pagas ni suscripciones
- 3 formas de uso: CLI, API REST, Integración Python
- Funciona en CPU (lento) o GPU (rápido)
- Modelos open-source de Hugging Face

## Quick Start

```bash
# 1. Instalar dependencias
pip install torch transformers diffusers accelerate pillow fastapi uvicorn pydantic

# 2. Generar un diseño (CLI)
python main.py --style rustic --space facade --size medium --colors "grey,beige"

# 3. Usar ejemplos predefinidos
python example_usage.py 2

# 4. Iniciar API REST (opcional)
python api/main.py
```

## Installation

### Prerequisites
- **Python 3.8+**
- **RAM**: 4-8GB mínimo (CPU), 8-16GB recomendado (GPU)
- **Disk**: 10GB libres (6GB para modelos + outputs)
- **GPU (opcional)**: NVIDIA con CUDA para procesamiento rápido

### Paso a Paso

1. **Navegar al directorio del proyecto:**
```bash
cd src
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

3. **Instalar PyTorch** (elegir según tu sistema):
```bash
# Solo CPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Con GPU CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Con GPU CUDA 12.1+
pip install torch torchvision
```

4. **Instalar dependencias restantes:**
```bash
# Para generación de diseños
pip install transformers diffusers accelerate pillow

# Para API REST (opcional)
pip install fastapi uvicorn pydantic
```

O instalar todo desde requirements.txt:
```bash
pip install -r requirements.txt
```

### Primera Ejecución

En el primer uso, el sistema descarga automáticamente:
- **FLAN-T5-base** (~1GB) - generación de texto
- **Stable Diffusion v1.5** (~5GB) - generación de imágenes

Tiempo estimado: 10-20 minutos según conexión a internet.
Los modelos se cachean en `~/.cache/huggingface/` y se reusan.

## How to Run

### Option 1: CLI (Línea de Comandos) - Recomendado

Genera especificaciones y renders usando argumentos de línea de comandos:

```bash
# Uso básico: genera especificación + render
python main.py --style rustic --space facade --size medium --colors "grey,beige"

# Solo especificación (más rápido, sin render)
python main.py --style rustic --space facade --size medium --colors "grey,beige" --no-render

# Más ejemplos
python main.py --style brutalism --space living_room --size small --colors "grey"
python main.py --style minimalist --space kitchen --size medium --colors "white,light grey"
python main.py --style industrial --space facade --size large --colors "grey,black"

# Ajustar calidad del render (más steps = mejor calidad, más lento)
python main.py --style rustic --space facade --size medium --colors "grey,beige" --steps 100
```

Resultados guardados en:
- Especificaciones: `outputs/specifications/`
- Renders: `outputs/renders/`

### Option 2: Ejemplos Programáticos

Usa el archivo de ejemplos para casos predefinidos:

```bash
# Ejemplo 1: Solo generación de texto
python example_usage.py 1

# Ejemplo 2: Pipeline completo (especificación + render)
python example_usage.py 2

# Ejemplo 3: Generar múltiples diseños
python example_usage.py 3
```

### Option 3: Integración en tu Código Python

Usa los generadores directamente en tu código:

```python
from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator

# Inicializar generadores
design_gen = DesignGenerator()
render_gen = RenderGenerator()

# Generar especificación
specification = design_gen.generate_specification(
    style="rustic",
    space="facade",
    size="medium",
    colors=["grey", "beige"]
)

print(specification)

# Opcionalmente, generar render
image, path = render_gen.generate_render(
    style="rustic",
    space="facade",
    specification=specification,
    colors=["grey", "beige"],
    filename="my_design.png",
    num_inference_steps=50
)

print(f"Render guardado en: {path}")
```

### Command Line Options

```bash
python main.py --help

Options:
  --style          Architectural style (required)
  --space          Space type (required)
  --size           Space size (required)
  --colors         Color palette, comma-separated (required)
  --no-render      Generate only specification, skip rendering
  --output-dir     Base directory for outputs (default: outputs)
  --steps          Inference steps for Stable Diffusion (default: 50)
  --guidance       Guidance scale for image generation (default: 7.5)
```

## Available Options

**Styles:**
- rustic (Rustic)
- brutalism (Brutalism)
- minimalist (Minimalist)
- industrial (Industrial)
- modern (Modern)
- mediterranean (Mediterranean)
- scandinavian (Scandinavian)
- contemporary_luxury (Contemporary Luxury)

**Spaces:**
- facade (Facade)
- living_room (Living room)
- kitchen (Kitchen)
- bathroom (Bathroom)
- bedroom (Bedroom)
- office (Office)
- restaurant (Restaurant)
- store (Store)

**Sizes:**
- small (Small < 20m²)
- medium (Medium 20-50m²)
- large (Large > 50m²)

## Project Structure

```
src/
├── api/
│   ├── __init__.py
│   ├── main.py                   # FastAPI REST API server
│   └── chat_handler.py           # Chat logic & topic validation
├── data/
│   ├── materials_catalog.json    # Materials database (150+ items)
│   └── system_prompt.txt         # System prompt for chat restrictions
├── models/
│   ├── design_generator.py       # Text generation (FLAN-T5-base)
│   ├── render_generator.py       # Image generation (Stable Diffusion)
│   └── chat_model.py             # Chat model with topic validation
├── outputs/
│   ├── specifications/           # Generated specs (.txt)
│   └── renders/                  # Generated renders (.png)
├── main.py                       # CLI principal (argparse)
├── example_usage.py              # Programmatic usage examples
├── requirements.txt              # Python dependencies
└── README.md                     # Este archivo
```

## Usage Examples

### Example 1: Fachada Rústica (Completo)
```bash
python main.py --style rustic --space facade --size medium --colors "grey,beige"
```
**Salida:**
- Especificación: `outputs/specifications/rustic_facade_medium.txt`
- Render: `outputs/renders/rustic_facade_medium.png`
- Materiales: Piedra natural, madera envejecida, estuco texturizado
- Paleta: Piedra gris, arena beige, acentos de madera

### Example 2: Sala Brutalista
```bash
python main.py --style brutalism --space living_room --size small --colors "grey"
```
**Salida:**
- Especificación con concreto expuesto, pisos pulidos, acentos industriales
- Render fotorrealista con iluminación dramática

### Example 3: Cocina Minimalista
```bash
python main.py --style minimalist --space kitchen --size medium --colors "white,light grey"
```
**Salida:**
- Porcelanato blanco, detalles en madera clara, líneas limpias
- Visualización arquitectónica de alta calidad

### Example 4: Solo Especificación (Rápido)
```bash
python main.py --style mediterranean --space facade --size large --colors "white,terracotta" --no-render
```
Genera solo la especificación técnica sin crear el render (útil para planificación).

### Example 5: Usando Ejemplos Programáticos
```bash
# Genera un diseño minimalista completo
python example_usage.py 2
```
Ejecuta el pipeline completo con parámetros predefinidos.

## Application Design & Architecture

### System Overview

El sistema ofrece **3 formas de uso** para adaptarse a diferentes necesidades:

1. **CLI (main.py)**: Interfaz de línea de comandos para generación rápida
2. **API REST (api/main.py)**: Chat especializado en terminaciones arquitectónicas
3. **Integración Python (example_usage.py)**: Uso programático de los modelos

Todos utilizan el mismo pipeline de dos etapas:

```
User Input → Text Generation → Image Generation → Output
  (Style,      (FLAN-T5-base)    (Stable          (Spec +
   Space,         250M params      Diffusion v1.5)  Render)
   Size,
   Colors)
```

### Architecture Components

#### 1. Data Layer (`data/`)
- **materials_catalog.json**: Comprehensive database of cladding materials with properties:
  - Material names and categories (wood, concrete, metal, etc.)
  - Physical properties (dimensions, finishes, textures)
  - Aesthetic attributes (colors, patterns)
  - Application contexts (exterior facades, interior walls, etc.)

#### 2. Text Generation Pipeline (`models/design_generator.py`)
- **Purpose**: Generate detailed technical specifications from user parameters
- **Technology**: FLAN-T5-base (Google, via Hugging Face)
- **Model Details**:
  - Encoder-decoder transformer architecture
  - Fine-tuned on instruction-following tasks
  - ~250M parameters
  - No API key required
- **Process**:
  1. Accepts user input (style, space, size, colors)
  2. Queries materials catalog for appropriate materials
  3. Uses FLAN-T5 to generate each specification section:
     - Project overview and design philosophy
     - Material recommendations with descriptions
     - Color palette strategy
     - Installation patterns and techniques
     - Technical requirements
     - Budget estimation
  4. Falls back to template generation if model fails
- **Output**: Text-based specification file saved to `outputs/specifications/`
- **Performance**: 30-60 seconds on CPU, 5-10 seconds on GPU

#### 3. Image Generation Pipeline (`models/render_generator.py`)
- **Purpose**: Create photorealistic renders from specifications
- **Technology**: Stable Diffusion model
- **Process**:
  1. Reads generated specification
  2. Constructs optimized prompt for image model
  3. Generates high-quality architectural visualization
  4. Post-processes image for consistency
- **Output**: Image file saved to `outputs/renders/`

### Data Flow

```
                    ┌─────────────────┐
                    │   User Input    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              v              v              v
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │ CLI      │   │ API REST │   │ Python   │
       │ main.py  │   │ FastAPI  │   │ examples │
       └─────┬────┘   └─────┬────┘   └─────┬────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                            v
              ┌─────────────────────────┐
              │  Design Generator       │
              │  - FLAN-T5-base model   │
              │  - Materials catalog    │
              │  - Generate spec        │
              └────────┬────────────────┘
                       │
                       v
              ┌─────────────────────────┐
              │  Specification (.txt)   │
              └────────┬────────────────┘
                       │
                       v
              ┌─────────────────────────┐
              │  Render Generator       │
              │  - Stable Diffusion     │
              │  - Create prompt        │
              │  - Generate image       │
              └────────┬────────────────┘
                       │
                       v
              ┌─────────────────────────┐
              │   Output (.png + .txt)  │
              └─────────────────────────┘
```

### Design Decisions

1. **Múltiples Interfaces**: CLI, API REST, y Python directo para diferentes casos de uso
2. **Pipeline Modular**: Generación de texto e imagen independientes permite desarrollo y testing separado
3. **Catálogo de Materiales**: Base de datos garantiza especificaciones realistas y construibles
4. **Modelos Open-Source**: FLAN-T5 y Stable Diffusion - sin APIs pagas ni límites de uso
5. **Topic Validation**: API con validación de temas para enfoque especializado
6. **Salidas Estructuradas**: Formatos estandarizados (.txt, .png) para integración fácil

### Technology Stack

- **Language**: Python 3.8+
- **Deep Learning Models**:
  - FLAN-T5-base: Text generation (google/flan-t5-base)
  - Stable Diffusion v1.5: Image generation (runwayml/stable-diffusion-v1-5)
- **AI/ML Frameworks**:
  - PyTorch: Deep learning foundation
  - Transformers (Hugging Face): Model loading and inference
  - Diffusers: Stable Diffusion pipeline
  - Accelerate: Model optimization
- **Data Processing**: JSON-based material catalog
- **Image Processing**: Pillow (PIL)
- **Storage**: File-based outputs (specifications as .txt, renders as .png)
- **Cost**: 100% free, no API keys or subscriptions required

### Development Roadmap

**Phase 1**: Text Generation Pipeline ✅
- Material catalog design
- Specification generator implementation
- FLAN-T5-base integration
- CLI interface (main.py)
- Example usage scripts

**Phase 2**: Image Generation Pipeline ✅
- Stable Diffusion v1.5 integration
- Prompt engineering for architectural renders
- Image quality optimization
- Complete pipeline integration

**Phase 3**: REST API & Chat ✅
- FastAPI REST API
- Chat model for architectural finishes
- Topic validation system
- Material recommendations
- Multi-endpoint architecture

**Future Enhancements**:
- Frontend web interface
- User sessions and conversation history
- Database persistence
- 3D model generation
- Real-time cost estimation
- Multi-language support

### Output Examples

**Specification Output** (`outputs/specifications/`):
```
Cladding for Rustic Style Facade (Medium: 20-50m²)

Primary Materials:
- Weathered Wood: Pine or oak planks with natural finish...
- Natural Stone: Limestone decorative elements...

Installation Pattern: Horizontal with irregular joints...
```

**Render Output** (`outputs/renders/`):
- High-resolution photorealistic architectural visualization
- Accurate material representation
- Contextual environment and lighting

## Performance Notes

### Hardware Requirements

**Minimum (CPU-only):**
- CPU: 4 cores
- RAM: 4-8GB
- Disk: 10GB free space (6GB for models, rest for outputs)
- Generation time:
  - Text: 30-60 seconds
  - Image: 2-4 minutes
  - Total: ~3-5 minutes per complete design

**Recommended (with GPU):**
- GPU: NVIDIA with 6GB+ VRAM (CUDA support)
- RAM: 8-16GB
- Disk: 15GB free space
- Generation time:
  - Text: 5-10 seconds
  - Image: 30-60 seconds
  - Total: ~1 minute per complete design

### Optimization Tips

1. **First run downloads models** (~6GB total: 1GB FLAN-T5 + 5GB Stable Diffusion)
   - Models are cached in `~/.cache/huggingface/`
   - Subsequent runs are much faster
2. **Use GPU when available** - automatic detection enabled
3. **Adjust inference steps** for image quality vs speed:
   - Fast: `--steps 20` (lower quality, ~1 min on CPU)
   - Balanced: `--steps 50` (default, ~3 min on CPU)
   - High quality: `--steps 100` (slower, ~5 min on CPU)
4. **Skip rendering for planning** - use `--no-render` flag for text-only
5. **CPU optimization**:
   - Close other applications to free RAM
   - FLAN-T5-base is optimized for CPU inference
   - Consider using `--steps 20` for faster iterations

### Troubleshooting

**Out of memory error:**
```bash
# Reduce inference steps
python main.py --style rustic --space facade --size medium --colors "grey" --steps 20
```

**Slow generation:**
- Ensure CUDA is properly installed for GPU acceleration
- First run is slower due to model downloads
- Subsequent runs use cached models

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade torch transformers diffusers accelerate pillow
```

**Model download fails:**
```bash
# Manually download models
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('google/flan-t5-base')"
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

**Hugging Face access (if needed):**
Both FLAN-T5-base and Stable Diffusion v1.5 are publicly available and don't require authentication. If you encounter access issues:
```bash
pip install huggingface_hub
huggingface-cli login
```

**Slow text generation:**
- FLAN-T5 generates text section by section (6 sections total)
- Each section takes 5-10 seconds on CPU
- This is normal for local model inference
- Consider using GPU for faster generation

---

## API de Chat para Terminaciones Arquitectónicas

### Descripción

La aplicación ahora incluye una **API REST con FastAPI** que funciona como un chat especializado en terminaciones arquitectónicas. El sistema está diseñado para responder ÚNICAMENTE preguntas sobre:

- **Enchapes** (cerámicos, porcelanatos, piedra natural, mosaicos)
- **Pinturas** (interiores, exteriores, acabados especiales)
- **Baños** (materiales, impermeabilización, griferías)
- **Pisos** (cerámicos, madera, vinílicos, laminados)
- **Acabados** arquitectónicos en general

El sistema valida automáticamente que las preguntas estén relacionadas con estos temas. Si el usuario pregunta sobre temas no relacionados, el sistema responde educadamente indicando su especialización.

### Instalación de Dependencias

Asegúrate de tener las dependencias de la API instaladas:

```bash
pip install fastapi uvicorn pydantic
```

O instala todas las dependencias desde requirements.txt:

```bash
pip install -r requirements.txt
```

### Cómo Ejecutar la API

Desde el directorio `src/`, ejecuta:

```bash
# Opción 1: Con uvicorn directamente
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Ejecutar el archivo Python
python api/main.py
```

La API estará disponible en: `http://localhost:8000`

### Documentación Automática

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Puedes usar estas interfaces para probar los endpoints directamente desde el navegador.

### Endpoints Disponibles

#### 1. GET `/` - Información de la API

```bash
curl http://localhost:8000/
```

Retorna información sobre la API y sus endpoints disponibles.

#### 2. GET `/health` - Estado del Servicio

```bash
curl http://localhost:8000/health
```

Verifica que el servicio esté funcionando correctamente.

**Respuesta:**
```json
{
  "status": "healthy",
  "message": "Terminaciones Chat API está funcionando correctamente"
}
```

#### 3. POST `/chat` - Enviar Mensaje al Chat

Endpoint principal para interactuar con el chat.

**Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué enchape recomiendas para un baño moderno?",
    "generate_image": false
  }'
```

**Parámetros:**
- `message` (string, requerido): Pregunta o mensaje del usuario
- `generate_image` (boolean, opcional): Si se debe generar una imagen (default: false)

**Respuesta:**
```json
{
  "response": "Para un baño moderno te recomiendo porcelanato de gran formato (60x120cm) en tonos grises o blancos...",
  "on_topic": true,
  "materials_suggested": [
    {
      "type": "ceramic_tile",
      "name": "Porcelain bathroom tile",
      "colors": ["white", "beige", "grey", "blue"],
      "price_range": "$25-45/m2"
    }
  ],
  "image_path": null
}
```

#### 4. GET `/materials/catalog` - Catálogo Completo

Obtiene el catálogo completo de materiales.

```bash
curl http://localhost:8000/materials/catalog
```

#### 5. GET `/materials/{category}` - Materiales por Categoría

Obtiene materiales filtrados por categoría.

**Categorías disponibles:**
- `bathroom_finishes` - Terminaciones para baños
- `paints` - Pinturas
- `flooring` - Pisos

```bash
# Ejemplo: obtener materiales de baño
curl http://localhost:8000/materials/bathroom_finishes

# Ejemplo: obtener pinturas
curl http://localhost:8000/materials/paints

# Ejemplo: obtener pisos
curl http://localhost:8000/materials/flooring
```

### Ejemplos de Uso

#### Ejemplo 1: Pregunta sobre Enchapes de Baño

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué tipo de enchape es mejor para la ducha?",
    "generate_image": false
  }'
```

**Respuesta:** El sistema responderá con recomendaciones específicas de porcelanato, información sobre impermeabilización, y precios.

#### Ejemplo 2: Pregunta sobre Pinturas

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué pintura uso para exteriores?",
    "generate_image": false
  }'
```

**Respuesta:** Recomendaciones de pinturas látex exterior o elastoméricas con durabilidad y precios.

#### Ejemplo 3: Pregunta Fuera de Tema

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cómo construyo una casa?",
    "generate_image": false
  }'
```

**Respuesta:**
```json
{
  "response": "Me especializo únicamente en terminaciones arquitectónicas como enchapes, pinturas, baños y acabados. ¿Puedo ayudarte con alguno de estos temas?",
  "on_topic": false,
  "materials_suggested": [],
  "image_path": null
}
```

#### Ejemplo 4: Generar Imagen (Opcional)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Dame una especificación completa para un baño minimalista",
    "generate_image": true
  }'
```

Esto generará tanto la respuesta de texto como una visualización usando Stable Diffusion (toma más tiempo).

### Usar desde Python

```python
import requests

# URL base de la API
base_url = "http://localhost:8000"

# Ejemplo 1: Enviar mensaje al chat
response = requests.post(
    f"{base_url}/chat",
    json={
        "message": "¿Qué enchape recomiendas para cocina?",
        "generate_image": False
    }
)

result = response.json()
print(result["response"])
print(result["materials_suggested"])

# Ejemplo 2: Obtener catálogo de materiales
catalog_response = requests.get(f"{base_url}/materials/catalog")
catalog = catalog_response.json()
print(catalog.keys())

# Ejemplo 3: Obtener materiales de baño
bathroom_materials = requests.get(f"{base_url}/materials/bathroom_finishes")
materials = bathroom_materials.json()
print(materials)
```

### Validación de Temas

El sistema implementa validación automática de temas mediante:

1. **Lista de palabras clave**: Detecta términos relacionados con terminaciones (enchape, pintura, baño, piso, etc.)
2. **System prompt**: Instruye al modelo para enfocarse solo en terminaciones
3. **Respuesta de redirección**: Cuando detecta temas no relacionados, responde educadamente

**Palabras clave monitoreadas:**
- Enchapes: ceramica, porcelanato, azulejo, mosaico, revestimiento, piedra, marmol
- Pinturas: pintura, pintar, latex, esmalte, acabado, color
- Baños: baño, ducha, sanitario, griferia, impermeabilizacion
- Pisos: piso, suelo, floor, madera, laminado, vinil
- Acabados: acabado, terminacion, textura, estuco, zocalo

### Arquitectura de la API

El módulo `api/` implementa un servidor REST con FastAPI:

```
api/
├── main.py              # FastAPI app, endpoints, CORS config
└── chat_handler.py      # Lógica del chat y validación de temas

Integra con:
├── models/chat_model.py        # Modelo FLAN-T5 para chat
├── models/design_generator.py  # Generador de especificaciones
├── models/render_generator.py  # Generador de imágenes
└── data/
    ├── materials_catalog.json  # Catálogo expandido
    └── system_prompt.txt       # Restricciones de tema
```

### Notas de Rendimiento

- **Primera carga**: El modelo FLAN-T5 se carga al iniciar la API (30-60 segundos)
- **Respuestas de chat**: 5-10 segundos en CPU, 1-2 segundos en GPU
- **Generación de imágenes**: Solo si se solicita con `generate_image: true` (2-4 minutos en CPU)
- **Recomendación**: Para mejor rendimiento, usa GPU y deja `generate_image: false` para respuestas rápidas

### Próximos Pasos

Para mejoras futuras (no implementadas aún):
- Sesiones de usuario con historial de conversación
- Base de datos para persistencia
- Autenticación y rate limiting
- WebSockets para chat en tiempo real
- Frontend web interactivo

---

## Resumen de Comandos Principales

### Generación de Diseños

```bash
# Diseño completo (especificación + render)
python main.py --style rustic --space facade --size medium --colors "grey,beige"

# Solo especificación (rápido)
python main.py --style rustic --space facade --size medium --colors "grey,beige" --no-render

# Alta calidad (más lento)
python main.py --style rustic --space facade --size medium --colors "grey,beige" --steps 100

# Ejemplo programático
python example_usage.py 2
```

### API REST

```bash
# Iniciar servidor
python api/main.py

# Documentación interactiva
# http://localhost:8000/docs

# Enviar consulta
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué enchape recomiendas para baño moderno?", "generate_image": false}'
```

### Instalación

```bash
# Instalación completa
pip install torch transformers diffusers accelerate pillow fastapi uvicorn pydantic

# O desde requirements.txt
pip install -r requirements.txt
```

## Soporte

Para problemas o preguntas:
1. Revisa la sección [Troubleshooting](#troubleshooting)
2. Verifica los [Performance Notes](#performance-notes) para optimizar rendimiento
3. Revisa los [Usage Examples](#usage-examples) para casos de uso comunes

---

**Última actualización**: 2025-01-27
**Versión**: 1.0 - Proyecto Mid-Term Deep Learning CSAI-353

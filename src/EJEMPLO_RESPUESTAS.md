# Ejemplos de Respuestas del Chat API

## Formato de Respuesta Simplificado

Ahora el API devuelve **solo un párrafo conversacional** sin datos estructurados innecesarios.

### Estructura de Respuesta

```json
{
  "response": "Texto conversacional aquí...",
  "on_topic": true,
  "image_path": null
}
```

## Ejemplos de Consultas y Respuestas

### Ejemplo 1: Enchape para Baño Moderno

**Consulta:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué enchape recomiendas para un baño moderno?", "generate_image": false}'
```

**Respuesta:**
```json
{
  "response": "Para un baño moderno, te recomiendo considerar porcelain bathroom tile en tonos white, beige, que tiene un precio de $25-45/m2. Otra excelente alternativa es glass mosaic tiles disponible en multicolor y white, que también funciona muy bien para este tipo de aplicación. Ambas opciones ofrecen buena durabilidad y acabados de calidad.",
  "on_topic": true,
  "image_path": null
}
```

### Ejemplo 2: Pintura para Exteriores

**Consulta:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué pintura uso para exteriores?", "generate_image": false}'
```

**Respuesta:**
```json
{
  "response": "Para pintura de exteriores, te recomiendo considerar exterior latex paint, que tiene un precio de $25-45/liter. Otra excelente alternativa es elastomeric coating, que también funciona muy bien para este tipo de aplicación. Ambas opciones ofrecen buena durabilidad y acabados de calidad.",
  "on_topic": true,
  "image_path": null
}
```

### Ejemplo 3: Piso para Cocina

**Consulta:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Necesito un piso para cocina", "generate_image": false}'
```

**Respuesta:**
```json
{
  "response": "Para el piso de cocina, te recomiendo considerar porcelain floor tile en tonos grey, beige, que tiene un precio de $30-60/m2. Otra excelente alternativa es ceramic floor tile disponible en terracotta y grey, que también funciona muy bien para este tipo de aplicación. Ambas opciones ofrecen buena durabilidad y acabados de calidad.",
  "on_topic": true,
  "image_path": null
}
```

### Ejemplo 4: Pregunta Fuera de Tema

**Consulta:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo construyo una casa?", "generate_image": false}'
```

**Respuesta:**
```json
{
  "response": "Me especializo únicamente en terminaciones arquitectónicas como enchapes, pinturas, baños y acabados. ¿Puedo ayudarte con alguno de estos temas?",
  "on_topic": false,
  "image_path": null
}
```

## Ventajas del Nuevo Formato

✅ **Respuestas más naturales**: Todo en un párrafo fluido y conversacional
✅ **Sin datos innecesarios**: Ya no se muestra `materials_suggested` como array separado
✅ **Integración completa**: Materiales, precios y colores están integrados en el texto
✅ **Fácil de leer**: El usuario recibe información directa y clara
✅ **Respuestas contextuales**: Detecta el tipo de consulta y adapta la introducción

## Cómo Usar

```bash
# 1. Iniciar el servidor API
python api/main.py

# 2. En otra terminal, probar el chat
bash test_api_chat.sh

# O usar curl directamente
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tu pregunta aquí", "generate_image": false}'
```

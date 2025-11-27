#!/bin/bash

echo "=========================================="
echo "Testing Simplified Chat API Responses"
echo "=========================================="
echo ""

# Test 1: Baño moderno
echo "📝 Test 1: Enchape para baño moderno"
echo "------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué enchape recomiendas para un baño moderno?", "generate_image": false}' \
  -s | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Respuesta: {data['response']}\"); print(f\"On Topic: {data['on_topic']}\")"
echo ""
echo ""

# Test 2: Pintura exterior
echo "📝 Test 2: Pintura para exteriores"
echo "------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué pintura uso para exteriores?", "generate_image": false}' \
  -s | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Respuesta: {data['response']}\"); print(f\"On Topic: {data['on_topic']}\")"
echo ""
echo ""

# Test 3: Piso de cocina
echo "📝 Test 3: Piso para cocina"
echo "------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Necesito un piso para cocina", "generate_image": false}' \
  -s | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Respuesta: {data['response']}\"); print(f\"On Topic: {data['on_topic']}\")"
echo ""
echo ""

# Test 4: Pregunta fuera de tema
echo "📝 Test 4: Pregunta fuera de tema"
echo "------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo construyo una casa?", "generate_image": false}' \
  -s | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Respuesta: {data['response']}\"); print(f\"On Topic: {data['on_topic']}\")"
echo ""
echo ""

echo "=========================================="
echo "✅ Tests completados"
echo "=========================================="

import json
import os
from typing import Dict, List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class TerminacionesChatModel:

    def __init__(
        self,
        catalog_path: str = None,
        system_prompt_path: str = None,
        model_name: str = "google/flan-t5-base",
    ):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Initializing TerminacionesChatModel with {model_name}...")
        print(f"Device: {self.device}")

        # Load model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.tokenizer = None

        # Load materials catalog
        if catalog_path is None:
            catalog_path = os.path.join(
                os.path.dirname(__file__), "../data/materials_catalog.json"
            )

        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        # Load system prompt
        if system_prompt_path is None:
            system_prompt_path = os.path.join(
                os.path.dirname(__file__), "../data/system_prompt.txt"
            )

        with open(system_prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        # Keywords for topic validation
        self.terminaciones_keywords = [
            # Enchapes
            "enchape",
            "ceramica",
            "porcelanato",
            "azulejo",
            "mosaico",
            "revestimiento",
            "baldosa",
            "tile",
            "piedra",
            "marmol",
            "granito",
            # Pinturas
            "pintura",
            "pintar",
            "latex",
            "esmalte",
            "acabado",
            "color",
            # Baños
            "baño",
            "ducha",
            "shower",
            "sanitario",
            "griferia",
            "llave",
            "impermeabili",
            "humedad",
            # Pisos
            "piso",
            "suelo",
            "floor",
            "parquet",
            "madera",
            "laminado",
            "vinil",
            "ceramico",
            # Acabados generales
            "acabado",
            "terminacion",
            "finish",
            "textura",
            "superficie",
            "pared",
            "wall",
            "techo",
            "ceiling",
            "estuco",
            "zocalo",
            "moldura",
        ]

        print("TerminacionesChatModel ready")

    def validate_topic(self, message: str) -> bool:
        message_lower = message.lower()

        # Check for keywords
        for keyword in self.terminaciones_keywords:
            if keyword in message_lower:
                return True

        return False

    def generate_response(
        self, user_message: str, context: Optional[List[str]] = None
    ) -> Dict:
        # Validate topic
        if not self.validate_topic(user_message):
            return {
                "response": "Me especializo únicamente en terminaciones arquitectónicas como enchapes, pinturas, baños y acabados. ¿Puedo ayudarte con alguno de estos temas?",
                "on_topic": False,
                "materials_suggested": [],
            }

        # Generate response using model
        if self.model is None or self.tokenizer is None:
            return {
                "response": "El modelo no está disponible en este momento.",
                "on_topic": True,
                "materials_suggested": [],
            }

        try:
            # Build prompt with system context
            prompt = self._build_prompt(user_message, context)

            # Generate with model
            response_text = self._generate_with_model(prompt, max_length=300)

            # Extract relevant materials from catalog
            materials_suggested = self._extract_relevant_materials(user_message)

            # Enhance response with catalog information
            enhanced_response = self._enhance_response_with_catalog(
                response_text, materials_suggested
            )

            return {
                "response": enhanced_response,
                "on_topic": True,
                "materials_suggested": materials_suggested,
            }

        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "response": "Lo siento, hubo un error al generar la respuesta. ¿Puedes reformular tu pregunta?",
                "on_topic": True,
                "materials_suggested": [],
            }

    def _build_prompt(
        self, user_message: str, context: Optional[List[str]] = None
    ) -> str:
        prompt = f"""You are an expert in architectural finishes. Answer the following question professionally and technically.
Focus on: tiles, paints, bathrooms, flooring, and architectural finishes.

Question: {user_message}

Provide a helpful, concise answer with specific recommendations:"""

        if context:
            prompt = f"Previous context: {' '.join(context[-3:])}\n\n" + prompt

        return prompt

    def _generate_with_model(self, prompt: str, max_length: int = 300) -> str:
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True,
                temperature=0.7,
                do_sample=True,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()

    def _extract_relevant_materials(self, user_message: str) -> List[Dict]:
        materials = []
        message_lower = user_message.lower()

        # Check bathroom finishes
        if any(
            word in message_lower for word in ["baño", "bath", "ducha", "shower"]
        ):
            if "bathroom_finishes" in self.catalog:
                ceramics = self.catalog["bathroom_finishes"].get("ceramics", [])
                materials.extend(ceramics[:2])

        # Check paints
        if any(word in message_lower for word in ["pintura", "paint", "pintar"]):
            if "paints" in self.catalog:
                interior_paints = self.catalog["paints"].get("interior_paints", [])
                materials.extend(interior_paints[:2])

        # Check flooring
        if any(word in message_lower for word in ["piso", "floor", "suelo"]):
            if "flooring" in self.catalog:
                ceramic_floors = self.catalog["flooring"].get("ceramic_floors", [])
                materials.extend(ceramic_floors[:2])

        # Check styles (existing catalog)
        for style_name, style_data in self.catalog.get("styles", {}).items():
            if style_name in message_lower:
                style_materials = style_data.get("materials", [])
                materials.extend(style_materials[:2])

        return materials[:3]  # Limit to 3 materials

    def _enhance_response_with_catalog(
        self, response: str, materials: List[Dict]
    ) -> str:
        if not materials:
            return response

        enhanced = response + "\n\n"

        if materials:
            enhanced += "Materiales recomendados:\n"
            for i, material in enumerate(materials, 1):
                name = material.get("name", "Material")
                material_type = material.get("type", "").replace("_", " ").title()
                price = material.get("price_range", "Precio variable")

                enhanced += f"\n{i}. {name}"
                if material_type:
                    enhanced += f" ({material_type})"
                enhanced += f"\n   Precio: {price}"

                # Add colors if available
                colors = material.get("colors", [])
                if colors:
                    enhanced += f"\n   Colores: {', '.join(colors[:3])}"

                # Add application if available
                application = material.get("application", [])
                if application:
                    enhanced += f"\n   Aplicación: {', '.join(application[:3])}"

        return enhanced

    def get_materials_by_category(self, category: str) -> List[Dict]:
        if category == "bathroom_finishes":
            result = []
            bf = self.catalog.get("bathroom_finishes", {})
            result.extend(bf.get("ceramics", []))
            return result
        elif category == "paints":
            result = []
            paints = self.catalog.get("paints", {})
            result.extend(paints.get("interior_paints", []))
            result.extend(paints.get("exterior_paints", []))
            return result
        elif category == "flooring":
            result = []
            flooring = self.catalog.get("flooring", {})
            result.extend(flooring.get("ceramic_floors", []))
            result.extend(flooring.get("wood_floors", []))
            result.extend(flooring.get("vinyl_floors", []))
            return result
        else:
            return []

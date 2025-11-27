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
            # Baños y áreas húmedas
            "baño",
            "ducha",
            "shower",
            "sanitario",
            "griferia",
            "llave",
            "impermeabili",
            "humedad",
            "piscina",
            "pool",
            "spa",
            "jacuzzi",
            "alberca",
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
            # Espacios exteriores
            "terraza",
            "balcon",
            "patio",
            "exterior",
            "fachada",
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

        try:
            # Extract relevant materials from catalog
            materials_suggested = self._extract_relevant_materials(user_message)

            # Use AI model to generate initial response
            if self.model is not None and self.tokenizer is not None:
                ai_response = self._generate_ai_intro(user_message, materials_suggested)
            else:
                ai_response = None

            # Generate natural language response with AI intro
            response_text = self._generate_natural_response(
                user_message, materials_suggested, ai_intro=ai_response
            )

            return {
                "response": response_text,
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

    def _generate_ai_intro(
        self, user_message: str, materials: List[Dict]
    ) -> Optional[str]:
        """Use FLAN-T5 to generate a natural, contextual introduction"""
        try:
            # Create a context-aware prompt
            materials_context = ""
            if materials:
                material_names = [m.get("name", "") for m in materials[:2]]
                materials_context = f"Considering materials like {', '.join(material_names)}."

            prompt = f"""You are a helpful architectural finishes consultant. Answer this question naturally in Spanish (1-2 sentences).

Question: {user_message}
{materials_context}

Natural answer:"""

            inputs = self.tokenizer(
                prompt, return_tensors="pt", max_length=512, truncation=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=100,
                    min_length=15,
                    num_beams=4,
                    temperature=0.9,
                    do_sample=True,
                    top_p=0.95,
                    repetition_penalty=1.3,
                )

            generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated.strip() if len(generated.strip()) > 10 else None

        except Exception as e:
            print(f"Error generating AI intro: {e}")
            return None

    def _build_prompt(
        self, user_message: str, context: Optional[List[str]] = None
    ) -> str:
        prompt = f"""Answer this question about architectural finishes in Spanish. Be friendly and give a short recommendation.

Pregunta: {user_message}

Respuesta recomendada:"""

        if context:
            prompt = f"Contexto previo: {' '.join(context[-3:])}\n\n" + prompt

        return prompt

    def _generate_with_model(self, prompt: str, max_length: int = 150) -> str:
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                min_length=20,
                num_beams=4,
                early_stopping=True,
                temperature=0.8,
                do_sample=True,
                top_p=0.92,
                repetition_penalty=1.2,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()

    def _extract_relevant_materials(self, user_message: str) -> List[Dict]:
        materials = []
        message_lower = user_message.lower()

        # Check for specific water-related areas (piscina, spa, etc.)
        if any(word in message_lower for word in ["piscina", "pool", "spa", "jacuzzi", "alberca"]):
            # For pools/water areas, recommend ceramic/porcelain materials
            if "bathroom_finishes" in self.catalog:
                ceramics = self.catalog["bathroom_finishes"].get("ceramics", [])
                # Filter water-resistant materials
                materials.extend([m for m in ceramics if m.get("water_absorption") and float(m.get("water_absorption", "1%").replace("%", "").replace("<", "")) < 1][:2])

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
                # Check if exterior or interior
                if any(word in message_lower for word in ["exterior", "afuera", "outside", "fachada"]):
                    exterior_paints = self.catalog["paints"].get("exterior_paints", [])
                    materials.extend(exterior_paints[:2])
                else:
                    interior_paints = self.catalog["paints"].get("interior_paints", [])
                    materials.extend(interior_paints[:2])

        # Check flooring
        if any(word in message_lower for word in ["piso", "floor", "suelo"]):
            if "flooring" in self.catalog:
                ceramic_floors = self.catalog["flooring"].get("ceramic_floors", [])
                materials.extend(ceramic_floors[:2])

        # Check for outdoor/wet areas keywords
        if any(word in message_lower for word in ["exterior", "outdoor", "terraza", "balcon", "patio"]):
            if "flooring" in self.catalog:
                ceramic_floors = self.catalog["flooring"].get("ceramic_floors", [])
                materials.extend(ceramic_floors[:2])

        # Check styles (existing catalog)
        for style_name, style_data in self.catalog.get("styles", {}).items():
            if style_name in message_lower:
                style_materials = style_data.get("materials", [])
                materials.extend(style_materials[:2])

        return materials[:3]  # Limit to 3 materials

    def _generate_natural_response(
        self, user_message: str, materials: List[Dict], ai_intro: Optional[str] = None
    ) -> str:
        """Generate a natural language response with AI-generated intro and material details"""

        import random

        # Use AI-generated intro if available, otherwise generate contextual intro
        if ai_intro and len(ai_intro) > 10:
            intro = ai_intro + " "
        else:
            # Fallback: generate contextual intro with variety
            message_lower = user_message.lower()
            intros = []

            if any(word in message_lower for word in ["baño", "bath", "ducha", "shower"]):
                base = "baño"
                if "moderno" in message_lower:
                    base += " moderno"
                elif "rustic" in message_lower or "rústico" in message_lower:
                    base += " rústico"
                intros = [
                    f"Para un {base}, ",
                    f"Si buscas materiales para un {base}, ",
                    f"En el caso de un {base}, ",
                ]
            elif any(word in message_lower for word in ["pintura", "paint", "pintar"]):
                if any(word in message_lower for word in ["exterior", "afuera", "fachada"]):
                    intros = [
                        "Para pintura de exteriores, ",
                        "Si necesitas pintar el exterior, ",
                        "En cuanto a pinturas exteriores, ",
                    ]
                else:
                    intros = [
                        "Para pintura de interiores, ",
                        "Si quieres pintar interiores, ",
                        "Para espacios interiores, ",
                    ]
            elif any(word in message_lower for word in ["piso", "floor", "suelo"]):
                if "cocina" in message_lower:
                    intros = [
                        "Para el piso de cocina, ",
                        "Si buscas piso para la cocina, ",
                        "En cocinas, para el piso ",
                    ]
                else:
                    intros = [
                        "Para pisos, ",
                        "Si necesitas piso, ",
                        "En cuanto a pisos, ",
                    ]
            else:
                intros = [
                    "Para tu proyecto, ",
                    "En este caso, ",
                    "Te puedo ayudar: ",
                ]

            intro = random.choice(intros) if intros else "Para tu proyecto, "

        if not materials:
            # More varied responses when no materials found
            no_material_responses = [
                "te sugiero consultar con un especialista que pueda evaluar tu caso específico.",
                "lo ideal sería que un profesional evalúe las condiciones particulares de tu espacio.",
                "te recomiendo buscar asesoría profesional para encontrar la mejor solución.",
            ]
            return intro + random.choice(no_material_responses)

        # Generate response with materials
        if len(materials) == 1:
            material = materials[0]
            name = material.get("name", "este material")
            price = material.get("price_range", "precio variable")
            colors = material.get("colors", [])
            application = material.get("application", [])

            # Varied recommendation phrases
            rec_phrases = [
                f"te recomiendo usar {name.lower()}",
                f"una excelente opción es {name.lower()}",
                f"te sugiero {name.lower()}",
            ]
            response = intro + random.choice(rec_phrases)

            if application:
                response += f" que funciona muy bien para {' y '.join(application[:2])}"

            if colors and len(colors) > 1:
                response += f". Lo encuentras en tonos como {', '.join(colors[:3])}"
            elif colors:
                response += f" en tono {colors[0]}"

            response += f", con un precio aproximado de {price}. Es una opción confiable y de buena calidad."

        else:
            # Multiple materials with variety
            material1 = materials[0]
            name1 = material1.get("name", "material")
            colors1 = material1.get("colors", [])
            price1 = material1.get("price_range", "precio variable")

            rec_starts = [
                f"te recomiendo considerar {name1.lower()}",
                f"una buena opción es {name1.lower()}",
                f"podrías usar {name1.lower()}",
            ]
            response = intro + random.choice(rec_starts)

            if colors1:
                response += f" en tonos {', '.join(colors1[:2])}"

            response += f", que cuesta alrededor de {price1}"

            if len(materials) > 1:
                material2 = materials[1]
                name2 = material2.get("name", "material")
                colors2 = material2.get("colors", [])

                alt_phrases = [
                    f". Otra alternativa es {name2.lower()}",
                    f". También puedes considerar {name2.lower()}",
                    f". Como segunda opción, {name2.lower()}",
                ]
                response += random.choice(alt_phrases)

                if colors2:
                    response += f" disponible en {' y '.join(colors2[:2])}"

                response += f", que también da buenos resultados"

            endings = [
                ". Ambas son opciones confiables.",
                ". Las dos ofrecen buena durabilidad.",
                ". Cualquiera de las dos funciona bien.",
            ]
            response += random.choice(endings)

        return response

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

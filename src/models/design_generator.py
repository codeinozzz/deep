import json
import os
from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class DesignGenerator:
    """
    AI-powered design specification generator using FLAN-T5-base.
    Generates architectural specifications based on style, space, size, and colors.
    """

    def __init__(
        self, catalog_path: str = None, model_name: str = "google/flan-t5-base"
    ):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Initializing DesignGenerator with {model_name}...")
        print(f"Device: {self.device}")

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

        if catalog_path is None:
            catalog_path = os.path.join(
                os.path.dirname(__file__), "../data/materials_catalog.json"
            )

        with open(catalog_path, "r") as f:
            self.catalog = json.load(f)

        print("DesignGenerator ready")

    def generate_specification(
        self,
        style: str,
        space: str,
        size: str,
        colors: List[str],
        max_length: int = 512,
    ) -> str:
        """
        Generate architectural specification using FLAN-T5-base.

        Args:
            style: Architectural style (rustic, minimalist, etc)
            space: Space type (facade, living_room, etc)
            size: Size category (small, medium, large)
            colors: List of desired colors
            max_length: Maximum output length

        Returns:
            Generated specification as string
        """
        style_data = self.catalog["styles"].get(style, {})
        space_data = self.catalog["spaces"].get(space, {})
        size_data = self.catalog["sizes"].get(size, {})

        context = self._build_context(style_data, space_data, size_data)

        print(f"\nGenerating specification...")
        print(f"  Style: {style} | Space: {space} | Size: {size}")
        print(f"  Colors: {', '.join(colors)}")

        if self.model is None or self.tokenizer is None:
            print("Model not available, using template fallback")
            return self._fallback_generation(style, space, size, colors, context)

        try:
            specification_parts = []

            sections = [
                (
                    "overview",
                    self._generate_overview(style, space, size, colors, context),
                ),
                ("materials", self._generate_materials(style, colors, context)),
                ("palette", self._generate_palette(colors)),
                ("installation", self._generate_installation(style, context)),
                ("technical", self._generate_technical(space, context)),
                ("budget", self._generate_budget(size, context)),
            ]

            for section_name, section_content in sections:
                if section_content:
                    specification_parts.append(section_content)

            full_spec = "\n\n".join(specification_parts)

            if len(full_spec) < 200:
                print("Generated spec too short, using template fallback")
                return self._fallback_generation(style, space, size, colors, context)

            print(f"Specification generated ({len(full_spec)} characters)")
            return full_spec

        except Exception as e:
            print(f"Error during generation: {e}")
            print("Falling back to template generation")
            return self._fallback_generation(style, space, size, colors, context)

    def _generate_with_model(self, prompt: str, max_length: int = 150) -> str:
        """Generate text using FLAN-T5 model."""
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True,
                temperature=0.8,
                do_sample=True,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()

    def _generate_overview(
        self, style: str, space: str, size: str, colors: List[str], context: Dict
    ) -> str:
        """Generate project overview section."""
        style_name = context.get("style_name", style.title())
        space_name = space.replace("_", " ").title()
        size_range = context.get("size_range", "")
        characteristics = context.get("characteristics", "")

        prompt = f"""Write a professional architectural project overview for a {style_name} style {space_name} of {size} size ({size_range}).
Include the design philosophy focusing on {characteristics}.
Preferred colors: {', '.join(colors)}.
Keep it technical and professional."""

        try:
            overview_text = self._generate_with_model(prompt, max_length=200)

            overview = f"ARCHITECTURAL DESIGN SPECIFICATION\n"
            overview += f"{'=' * 60}\n\n"
            overview += f"PROJECT OVERVIEW\n"
            overview += f"Style: {style_name}\n"
            overview += f"Space: {space_name}\n"
            overview += f"Size: {size.title()} ({size_range})\n"
            overview += f"Color Palette: {', '.join(colors)}\n\n"
            overview += f"Design Philosophy:\n{overview_text}\n"
            overview += f"\nKey Characteristics: {characteristics}"

            return overview
        except Exception as e:
            print(f"Error generating overview: {e}")
            return self._template_overview(style, space, size, colors, context)

    def _generate_materials(self, style: str, colors: List[str], context: Dict) -> str:
        """Generate materials section."""
        materials = context.get("materials", [])

        if not materials:
            return ""

        section = "PRIMARY MATERIALS\n" + "-" * 60 + "\n\n"

        for idx, material in enumerate(materials[:3], 1):
            mat_name = material.get("name", "")
            mat_type = material.get("type", "").replace("_", " ").title()
            mat_colors = ", ".join(material.get("colors", []))
            mat_texture = material.get("texture", "")
            mat_finish = material.get("finish", "")
            price = material.get("price_range", "")

            prompt = f"""Describe the application of {mat_name} ({mat_type}) in {style} architecture.
Focus on texture ({mat_texture}), finish ({mat_finish}), and aesthetic impact.
Keep it concise and technical."""

            try:
                description = self._generate_with_model(prompt, max_length=120)
            except:
                description = f"High-quality {mat_type} providing {mat_texture} texture with {mat_finish} finish."

            section += f"{idx}. {mat_name.upper()}\n"
            section += f"   Type: {mat_type}\n"
            section += f"   Colors: {mat_colors}\n"
            section += f"   Texture: {mat_texture}\n"
            section += f"   Finish: {mat_finish}\n"
            section += f"   Application: {description}\n"
            section += f"   Price Range: {price}\n\n"

        return section

    def _generate_palette(self, colors: List[str]) -> str:
        """Generate color palette section."""
        section = "COLOR PALETTE\n" + "-" * 60 + "\n\n"

        prompt = f"""Explain how to use these colors in architectural design: {', '.join(colors)}.
Describe distribution, balance, and visual impact. Keep it professional."""

        try:
            palette_desc = self._generate_with_model(prompt, max_length=100)
        except:
            palette_desc = f"Balanced distribution of {', '.join(colors)} to create visual harmony and spatial definition."

        section += f"Selected Colors: {', '.join(colors)}\n\n"
        section += f"Color Strategy:\n{palette_desc}"

        return section

    def _generate_installation(self, style: str, context: Dict) -> str:
        """Generate installation pattern section."""
        section = "INSTALLATION PATTERN\n" + "-" * 60 + "\n\n"

        prompt = f"""Describe installation patterns and techniques for {style} style architecture.
Include layout, joint treatment, and special techniques. Be specific and technical."""

        try:
            installation = self._generate_with_model(prompt, max_length=120)
        except:
            installation = "Follow standard installation practices with attention to alignment, spacing, and proper sealing."

        section += installation

        return section

    def _generate_technical(self, space: str, context: Dict) -> str:
        """Generate technical specifications section."""
        considerations = context.get("considerations", [])

        section = "TECHNICAL SPECIFICATIONS\n" + "-" * 60 + "\n\n"

        space_name = space.replace("_", " ").title()
        prompt = f"""List technical requirements for {space_name} construction.
Include structural, weather protection, and maintenance needs. Be specific."""

        try:
            technical = self._generate_with_model(prompt, max_length=120)
            section += f"{technical}\n\n"
        except:
            section += f"Standard technical requirements apply.\n\n"

        if considerations:
            section += "Key Considerations:\n"
            for cons in considerations:
                section += f"  - {cons}\n"

        return section

    def _generate_budget(self, size: str, context: Dict) -> str:
        """Generate budget estimation section."""
        section = "ESTIMATED BUDGET\n" + "-" * 60 + "\n\n"

        materials = context.get("materials", [])
        if not materials:
            return section + "Budget estimate: Varies based on material selection"

        size_range = context.get("size_range", "")

        prices = []
        for mat in materials[:3]:
            price_str = mat.get("price_range", "")
            if price_str:
                try:
                    price_parts = price_str.replace("$", "").split("-")
                    if len(price_parts) == 2:
                        avg_price = (
                            float(price_parts[0]) + float(price_parts[1].split("/")[0])
                        ) / 2
                        prices.append(avg_price)
                except:
                    pass

        if prices:
            avg_budget = sum(prices) / len(prices)
            section += f"Average Material Cost: ${avg_budget:.0f}/m²\n"
            section += f"Size Range: {size_range}\n"

            if size == "small":
                area = 15
            elif size == "medium":
                area = 35
            else:
                area = 60

            total = avg_budget * area
            section += (
                f"Estimated Total (approx {area}m²): ${total:.0f} - ${total*1.3:.0f}"
            )
        else:
            section += "Budget estimate available upon material selection"

        return section

    def _build_context(
        self, style_data: Dict, space_data: Dict, size_data: Dict
    ) -> Dict:
        """Build context dictionary from catalog data."""
        context = {}

        if style_data:
            context["style_name"] = style_data.get("name", "")
            context["characteristics"] = style_data.get("characteristics", "")
            context["palette"] = style_data.get("palette", [])

            materials = style_data.get("materials", [])
            context["materials"] = [
                {
                    "name": m.get("name", ""),
                    "type": m.get("type", ""),
                    "colors": m.get("colors", []),
                    "texture": m.get("texture", ""),
                    "finish": m.get("finish", ""),
                    "price_range": m.get("price_range", ""),
                }
                for m in materials[:3]
            ]

        if space_data:
            context["space_type"] = space_data.get("type", "")
            context["considerations"] = space_data.get("considerations", [])

        if size_data:
            context["size_range"] = size_data.get("range", "")
            context["optimization"] = size_data.get("optimization", [])

        return context

    def _template_overview(
        self, style: str, space: str, size: str, colors: List[str], context: Dict
    ) -> str:
        """Template-based overview generation."""
        style_name = context.get("style_name", style.title())
        space_name = space.replace("_", " ").title()
        size_range = context.get("size_range", "")
        characteristics = context.get("characteristics", "")

        overview = f"ARCHITECTURAL DESIGN SPECIFICATION\n"
        overview += f"{'=' * 60}\n\n"
        overview += f"PROJECT OVERVIEW\n"
        overview += f"Style: {style_name}\n"
        overview += f"Space: {space_name}\n"
        overview += f"Size: {size.title()} ({size_range})\n"
        overview += f"Color Palette: {', '.join(colors)}\n\n"
        overview += f"This {style_name} design emphasizes {characteristics}.\n"
        overview += f"The {space_name} is designed with {size} proportions in mind."

        return overview

    def _fallback_generation(
        self, style: str, space: str, size: str, colors: List[str], context: Dict
    ) -> str:
        """Complete template-based generation fallback."""
        spec = f"ARCHITECTURAL DESIGN SPECIFICATION\n"
        spec += f"{'=' * 60}\n\n"

        style_name = context.get("style_name", style.title())
        space_name = space.replace("_", " ").title()
        size_range = context.get("size_range", "")
        characteristics = context.get("characteristics", "")

        spec += f"PROJECT OVERVIEW\n"
        spec += f"Style: {style_name}\n"
        spec += f"Space: {space_name}\n"
        spec += f"Size: {size.title()} ({size_range})\n"
        spec += f"Characteristics: {characteristics}\n\n"

        spec += f"PRIMARY MATERIALS\n" + "-" * 60 + "\n\n"
        for idx, material in enumerate(context.get("materials", [])[:3], 1):
            spec += f"{idx}. {material['name'].upper()}\n"
            spec += f"   Type: {material['type'].replace('_', ' ').title()}\n"
            spec += f"   Colors: {', '.join(material['colors'])}\n"
            spec += f"   Texture: {material['texture']}\n"
            spec += f"   Finish: {material['finish']}\n"
            spec += f"   Price: {material['price_range']}\n\n"

        spec += f"COLOR PALETTE\n" + "-" * 60 + "\n"
        for color in colors:
            spec += f"  - {color}\n"

        spec += f"\nTECHNICAL CONSIDERATIONS\n" + "-" * 60 + "\n"
        for cons in context.get("considerations", []):
            spec += f"  - {cons}\n"

        spec += f"\nOPTIMIZATION STRATEGIES\n" + "-" * 60 + "\n"
        for opt in context.get("optimization", []):
            spec += f"  - {opt}\n"

        return spec

    def get_available_options(self) -> Dict:
        """Get all available design options from catalog."""
        return {
            "styles": list(self.catalog["styles"].keys()),
            "spaces": list(self.catalog["spaces"].keys()),
            "sizes": list(self.catalog["sizes"].keys()),
        }

import json
import os
from typing import List, Dict, Optional

class DesignGenerator:
    def __init__(self, catalog_path: str = None):
        if catalog_path is None:
            catalog_path = os.path.join(
                os.path.dirname(__file__),
                "../data/materials_catalog.json"
            )

        with open(catalog_path, 'r') as f:
            self.catalog = json.load(f)

    def generate_specification(
        self,
        style: str,
        space: str,
        size: str,
        colors: List[str]
    ) -> str:

        style_data = self.catalog["styles"].get(style)
        space_data = self.catalog["spaces"].get(space)
        size_data = self.catalog["sizes"].get(size)

        if not all([style_data, space_data, size_data]):
            return "Error: Invalid style, space, or size"

        materials = self._select_materials(style_data, space_data, colors)

        spec = self._build_specification(
            style_data=style_data,
            space_data=space_data,
            size_data=size_data,
            materials=materials,
            space_name=space,
            size_name=size
        )

        return spec

    def _select_materials(
        self,
        style_data: Dict,
        space_data: Dict,
        colors: List[str]
    ) -> List[Dict]:

        available_materials = style_data["materials"]
        space_type = space_data["type"].split("_")[0]

        filtered_materials = [
            m for m in available_materials
            if space_type in m["application"]
        ]

        if not filtered_materials:
            filtered_materials = [
                m for m in available_materials
                if "interior" in m["application"]
            ]

        if not filtered_materials:
            filtered_materials = available_materials

        if colors:
            color_matched = []
            for material in filtered_materials:
                if any(color.lower() in " ".join(material["colors"]).lower()
                       for color in colors):
                    color_matched.append(material)

            if color_matched:
                filtered_materials = color_matched

        return filtered_materials[:3] if len(filtered_materials) >= 3 else filtered_materials

    def _build_specification(
        self,
        style_data: Dict,
        space_data: Dict,
        size_data: Dict,
        materials: List[Dict],
        space_name: str,
        size_name: str
    ) -> str:

        space_display = space_data["type"].replace("_", " ").title()
        size_range = size_data["range"]

        spec = f"DESIGN SPECIFICATION - {style_data['name'].upper()} STYLE\n\n"
        spec += f"SPACE DETAILS:\n"
        spec += f"Type: {space_display}\n"
        spec += f"Size: {size_name.title()} ({size_range})\n"
        spec += f"Style: {style_data['name']}\n"
        spec += f"Characteristics: {style_data['characteristics']}\n\n"

        spec += f"PRIMARY MATERIALS:\n\n"

        for idx, material in enumerate(materials, 1):
            spec += f"{idx}. {material['name'].upper()} ({material['type'].replace('_', ' ').title()})\n"
            spec += f"   Colors: {', '.join(material['colors'])}\n"
            spec += f"   Texture: {material['texture']}\n"
            spec += f"   Finish: {material['finish']}\n"
            spec += f"   Application: {', '.join(material['application'])}\n"
            spec += f"   Coverage: {material['coverage']}\n"
            spec += f"   Price: {material['price_range']}\n\n"

        spec += f"COLOR PALETTE:\n"
        for idx, color in enumerate(style_data["palette"][:4], 1):
            spec += f"  {idx}. {color}\n"

        spec += f"\nSPACE OPTIMIZATION ({size_name.upper()}):\n"
        for opt in size_data["optimization"]:
            spec += f"  - {opt}\n"

        spec += f"\nTECHNICAL CONSIDERATIONS:\n"
        for cons in space_data["considerations"]:
            spec += f"  - {cons}\n"

        total_price = self._estimate_price(materials, size_name)
        spec += f"\nESTIMATED BUDGET: ${total_price[0]}-{total_price[1]}/m2\n"

        spec += f"\nMAINTENANCE:\n"
        spec += self._get_maintenance_notes(materials)

        return spec

    def _estimate_price(self, materials: List[Dict], size: str) -> tuple:

        prices = []
        for material in materials:
            price_str = material["price_range"].replace("$", "").replace("/m2", "")
            low, high = map(int, price_str.split("-"))
            prices.append((low, high))

        if not prices:
            return (100, 200)

        avg_low = sum(p[0] for p in prices) // len(prices)
        avg_high = sum(p[1] for p in prices) // len(prices)

        multiplier = {"pequeno": 1.2, "mediano": 1.0, "grande": 0.9}
        factor = multiplier.get(size, 1.0)

        return (int(avg_low * factor), int(avg_high * factor))

    def _get_maintenance_notes(self, materials: List[Dict]) -> str:

        maintenance_map = {
            "stone": "Annual cleaning, re-seal every 2 years",
            "wood": "Varnish/oil treatment every 12-18 months",
            "concrete": "Low maintenance, occasional sealing",
            "metal": "Corrosion check annually, clean as needed",
            "ceramic": "Regular cleaning, grout maintenance",
            "porcelain": "Minimal maintenance, easy cleaning",
            "glass": "Regular cleaning, check seals",
            "stucco": "Touch-up as needed, wash annually"
        }

        notes = ""
        for material in materials:
            mat_type = material["type"].split("_")[0]
            if mat_type in maintenance_map:
                notes += f"  - {material['name']}: {maintenance_map[mat_type]}\n"

        return notes if notes else "  - Standard maintenance per manufacturer specs\n"

    def get_available_options(self) -> Dict:

        return {
            "styles": list(self.catalog["styles"].keys()),
            "spaces": list(self.catalog["spaces"].keys()),
            "sizes": list(self.catalog["sizes"].keys())
        }

import os
from typing import Optional
from models.chat_model import TerminacionesChatModel
from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator


class ChatHandler:

    def __init__(self):
        print("Initializing ChatHandler...")

        # Initialize chat model
        self.chat_model = TerminacionesChatModel()

        # Initialize design and render generators (lazy loading)
        self.design_generator = None
        self.render_generator = None

        print("ChatHandler ready")

    def process_message(
        self, message: str, generate_image: bool = False
    ) -> dict:
        print(f"\nProcessing message: {message}")
        print(f"Generate image: {generate_image}")

        # Generate chat response
        response_data = self.chat_model.generate_response(message)

        result = {
            "response": response_data["response"],
            "on_topic": response_data["on_topic"],
            "materials_suggested": response_data["materials_suggested"],
            "image_path": None,
        }

        # If not on topic, return early
        if not response_data["on_topic"]:
            return result

        # Generate image if requested and topic is valid
        if generate_image:
            print("Image generation requested...")

            # Check if message contains specification request
            if self._is_specification_request(message):
                image_path = self._generate_full_specification(message)
                result["image_path"] = image_path
            else:
                # Generate simple image based on materials suggested
                if response_data["materials_suggested"]:
                    image_path = self._generate_material_visualization(
                        response_data["materials_suggested"]
                    )
                    result["image_path"] = image_path

        return result

    def _is_specification_request(self, message: str) -> bool:
        spec_keywords = [
            "especificacion",
            "specification",
            "diseño completo",
            "complete design",
            "proyecto",
            "project",
            "render",
            "visualizacion",
            "generar diseño",
        ]

        message_lower = message.lower()
        return any(keyword in message_lower for keyword in spec_keywords)

    def _generate_full_specification(self, message: str) -> Optional[str]:
        try:
            # Initialize generators if needed
            if self.design_generator is None:
                self.design_generator = DesignGenerator()

            if self.render_generator is None:
                self.render_generator = RenderGenerator()

            # Extract parameters from message (simple heuristic)
            # Default values
            style = "minimalist"
            space = "bathroom"
            size = "medium"
            colors = ["white", "grey"]

            # Try to detect style
            if "rustic" in message.lower():
                style = "rustic"
            elif "industrial" in message.lower():
                style = "industrial"
            elif "brutalism" in message.lower():
                style = "brutalism"

            # Try to detect space
            if "baño" in message.lower() or "bathroom" in message.lower():
                space = "bathroom"
            elif "cocina" in message.lower() or "kitchen" in message.lower():
                space = "kitchen"
            elif "sala" in message.lower() or "living" in message.lower():
                space = "living_room"

            # Generate specification
            specification = self.design_generator.generate_specification(
                style=style, space=space, size=size, colors=colors
            )

            # Generate render
            output_dir = os.path.join(
                os.path.dirname(__file__), "../outputs/chat_renders"
            )
            os.makedirs(output_dir, exist_ok=True)

            filename = f"chat_{style}_{space}.png"

            image, render_path = self.render_generator.generate_render(
                style=style,
                space=space,
                specification=specification,
                colors=colors,
                output_dir=output_dir,
                filename=filename,
            )

            return render_path

        except Exception as e:
            print(f"Error generating full specification: {e}")
            return None

    def _generate_material_visualization(
        self, materials: list
    ) -> Optional[str]:
        return None

    def get_materials_catalog(self) -> dict:
        return self.chat_model.catalog

    def get_materials_by_category(self, category: str) -> list:
        return self.chat_model.get_materials_by_category(category)

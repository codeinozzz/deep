import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os

class RenderGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device=None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        print(f"Loading Stable Diffusion on {self.device}...")

        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None
        )
        self.pipe = self.pipe.to(self.device)

        if self.device == "cuda":
            self.pipe.enable_attention_slicing()

        print("Model loaded successfully")

    def _build_prompt(self, style, space, specification, colors=None):
        style_prompts = {
            "rustic": "rustic architectural design, natural stone cladding, weathered wood texture, organic materials, warm lighting",
            "brutalism": "brutalist architecture, exposed concrete walls, raw materials, geometric shapes, dramatic lighting, modern design",
            "minimalist": "minimalist interior design, clean lines, smooth surfaces, white walls, simple elegant, natural light",
            "industrial": "industrial style, exposed brick walls, metal accents, urban design, loft aesthetic, Edison lighting",
            "modern": "modern contemporary architecture, sleek materials, glass and steel, clean geometric design, professional lighting",
            "mediterranean": "mediterranean architecture, stucco walls, terracotta accents, warm earth tones, soft textures, natural lighting",
            "scandinavian": "scandinavian design, light wood, white walls, cozy atmosphere, natural materials, bright airy space",
            "contemporary_luxury": "luxury contemporary design, marble surfaces, premium materials, elegant sophisticated, ambient lighting"
        }

        space_prompts = {
            "facade": "exterior facade view, architectural photography, building exterior, professional real estate photography",
            "living_room": "living room interior, residential space, comfortable seating area, interior design photography",
            "kitchen": "modern kitchen interior, culinary space, functional design, interior architecture",
            "bathroom": "bathroom interior, spa-like atmosphere, clean design, interior photography",
            "bedroom": "bedroom interior, sleeping area, peaceful atmosphere, residential design",
            "office": "office interior, workspace design, professional environment, commercial interior",
            "restaurant": "restaurant interior, dining space, hospitality design, commercial photography",
            "store": "retail store interior, commercial space, display area, shop design"
        }

        base_prompt = f"{style_prompts.get(style, 'architectural design')}, {space_prompts.get(space, 'interior space')}"

        if colors:
            color_str = " ".join(colors)
            base_prompt += f", {color_str} color palette"

        base_prompt += ", photorealistic, high quality, architectural digest style, professional photography, 8k, detailed textures, realistic materials"

        negative_prompt = "blurry, low quality, distorted, cartoon, anime, painting, sketch, unrealistic, oversaturated, people, humans, text, watermark, signature"

        return base_prompt, negative_prompt

    def generate_render(self, style, space, specification, colors=None,
                       output_dir="outputs/renders", filename=None,
                       num_inference_steps=50, guidance_scale=7.5):

        os.makedirs(output_dir, exist_ok=True)

        prompt, negative_prompt = self._build_prompt(style, space, specification, colors)

        print(f"\nGenerating render: {style} {space}")
        print(f"Prompt: {prompt[:100]}...")

        with torch.inference_mode():
            image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=768,
                width=768
            ).images[0]

        if filename is None:
            filename = f"{style}_{space}_render.png"

        output_path = os.path.join(output_dir, filename)
        image.save(output_path)

        print(f"Render saved: {output_path}")

        return image, output_path

    def generate_from_spec_file(self, spec_file_path, style, space, colors=None):
        with open(spec_file_path, 'r', encoding='utf-8') as f:
            specification = f.read()

        filename = os.path.basename(spec_file_path).replace('.txt', '_render.png')

        return self.generate_render(style, space, specification, colors, filename=filename)

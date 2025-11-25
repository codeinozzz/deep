from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator
import os

def test_complete_pipeline():
    test_cases = [
        {
            "name": "Rustic Facade",
            "style": "rustic",
            "space": "facade",
            "size": "medium",
            "colors": ["grey", "beige"]
        },
        {
            "name": "Brutalist Living Room",
            "style": "brutalism",
            "space": "living_room",
            "size": "small",
            "colors": ["grey"]
        },
        {
            "name": "Minimalist Kitchen",
            "style": "minimalist",
            "space": "kitchen",
            "size": "medium",
            "colors": ["white", "light wood"]
        },
        {
            "name": "Industrial Office",
            "style": "industrial",
            "space": "office",
            "size": "large",
            "colors": ["grey", "black", "brick"]
        },
        {
            "name": "Mediterranean Facade",
            "style": "mediterranean",
            "space": "facade",
            "size": "medium",
            "colors": ["white", "terracotta"]
        }
    ]

    print("="*80)
    print("COMPLETE TEST: SPECIFICATIONS + RENDERS")
    print("="*80)

    design_gen = DesignGenerator()
    render_gen = RenderGenerator()

    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {case['name']}")
        print("-"*80)

        specification = design_gen.generate_specification(
            style=case['style'],
            space=case['space'],
            size=case['size'],
            colors=case['colors']
        )

        spec_filename = f"{case['style']}_{case['space']}_{case['size']}.txt"
        spec_path = os.path.join("outputs/specifications", spec_filename)

        os.makedirs("outputs/specifications", exist_ok=True)
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(specification)

        print(f"Specification saved: {spec_path}")

        image, render_path = render_gen.generate_render(
            style=case['style'],
            space=case['space'],
            specification=specification,
            colors=case['colors'],
            filename=f"{case['style']}_{case['space']}_{case['size']}.png",
            num_inference_steps=30
        )

        print(f"Render saved: {render_path}")
        print(f"Resolution: {image.size[0]}x{image.size[1]}")

    print("\n" + "="*80)
    print(f"TEST COMPLETED: {len(test_cases)} designs generated")
    print("="*80)
    print("\nCheck the files in:")
    print("  - outputs/specifications/ (technical specifications)")
    print("  - outputs/renders/ (photorealistic renders)")
    print()

if __name__ == "__main__":
    test_complete_pipeline()

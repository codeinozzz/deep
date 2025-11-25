from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator

def example_text_only():
    print("Example 1: Specification generation only")
    print("-" * 60)

    generator = DesignGenerator()

    specification = generator.generate_specification(
        style="rustic",
        space="facade",
        size="medium",
        colors=["grey", "beige"]
    )

    print(specification)
    print("\n")

def example_complete_pipeline():
    print("Example 2: Complete pipeline (specification + render)")
    print("-" * 60)

    design_gen = DesignGenerator()
    render_gen = RenderGenerator()

    specification = design_gen.generate_specification(
        style="minimalist",
        space="kitchen",
        size="medium",
        colors=["white", "light grey"]
    )

    print("Specification generated")
    print(specification[:200] + "...\n")

    image, path = render_gen.generate_render(
        style="minimalist",
        space="kitchen",
        specification=specification,
        colors=["white", "light grey"],
        filename="example_minimalist_kitchen.png",
        num_inference_steps=30
    )

    print(f"Render saved at: {path}")
    print(f"Resolution: {image.size}\n")

def example_multiple_designs():
    print("Example 3: Generate multiple designs")
    print("-" * 60)

    design_gen = DesignGenerator()
    render_gen = RenderGenerator()

    designs = [
        ("brutalism", "living_room", "small", ["grey"]),
        ("mediterranean", "facade", "medium", ["white", "terracotta"])
    ]

    for style, space, size, colors in designs:
        print(f"\nGenerating: {style} {space} {size}")

        spec = design_gen.generate_specification(style, space, size, colors)

        image, path = render_gen.generate_render(
            style, space, spec, colors,
            filename=f"{style}_{space}_example.png",
            num_inference_steps=25
        )

        print(f"Completed: {path}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "1":
            example_text_only()
        elif sys.argv[1] == "2":
            example_complete_pipeline()
        elif sys.argv[1] == "3":
            example_multiple_designs()
    else:
        print("Usage:")
        print("  python example_usage.py 1  # Text only")
        print("  python example_usage.py 2  # Complete pipeline")
        print("  python example_usage.py 3  # Multiple designs")

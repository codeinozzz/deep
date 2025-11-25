import os
from typing import Any
from models.design_generator import DesignGenerator


def print_separator() -> None:
    print("\n" + "=" * 80 + "\n")


def run_tests() -> None:
    generator = DesignGenerator()

    test_cases: list[dict[str, Any]] = [
        {
            "name": "Rustic Facade - Medium",
            "style": "rustic",
            "space": "facade",
            "size": "medium",
            "colors": ["grey", "beige"],
        },
        {
            "name": "Brutalist Living Room - Small",
            "style": "brutalism",
            "space": "living_room",
            "size": "small",
            "colors": ["grey"],
        },
        {
            "name": "Minimalist Kitchen - Medium",
            "style": "minimalist",
            "space": "kitchen",
            "size": "medium",
            "colors": ["white", "light"],
        },
        {
            "name": "Industrial Office - Large",
            "style": "industrial",
            "space": "office",
            "size": "large",
            "colors": ["grey", "black"],
        },
        {
            "name": "Mediterranean Facade - Medium",
            "style": "mediterranean",
            "space": "facade",
            "size": "medium",
            "colors": ["white", "terracotta"],
        },
        {
            "name": "Scandinavian Bedroom - Small",
            "style": "scandinavian",
            "space": "bedroom",
            "size": "small",
            "colors": ["white", "light"],
        },
        {
            "name": "Contemporary Luxury Bathroom - Medium",
            "style": "contemporary_luxury",
            "space": "bathroom",
            "size": "medium",
            "colors": ["white", "gold"],
        },
        {
            "name": "Modern Restaurant - Large",
            "style": "modern",
            "space": "restaurant",
            "size": "large",
            "colors": ["grey", "white"],
        },
    ]

    print("CLADDING DESIGNER - TEST SUITE")
    print("Testing text generation pipeline with 8 design scenarios")
    print_separator()

    for idx, test in enumerate(test_cases, 1):
        print(f"TEST {idx}: {test['name']}")
        print_separator()

        specification = generator.generate_specification(
            style=str(test["style"]),
            space=str(test["space"]),
            size=str(test["size"]),
            colors=list(test["colors"]),
        )

        print(specification)
        print_separator()

        output_path = os.path.join(
            os.path.dirname(__file__),
            "outputs",
            "specifications",
            f"{test['style']}_{test['space']}_{test['size']}.txt",
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            f.write(specification)

        print(f"Saved to: {output_path}")
        print_separator()

    print("\nALL TESTS COMPLETED")
    print(f"Generated {len(test_cases)} design specifications")

    options = generator.get_available_options()
    print("\nAVAILABLE OPTIONS:")
    print(f"Styles: {', '.join(options['styles'])}")
    print(f"Spaces: {', '.join(options['spaces'])}")
    print(f"Sizes: {', '.join(options['sizes'])}")


if __name__ == "__main__":
    run_tests()

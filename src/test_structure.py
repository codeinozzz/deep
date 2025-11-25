#!/usr/bin/env python3
"""Quick structure test for DesignGenerator without loading models"""

from models.design_generator import DesignGenerator
import json
import os


def test_structure():
    """Test basic structure without model loading"""
    print("Testing DesignGenerator structure...")

    # Create instance without full initialization
    gen = DesignGenerator.__new__(DesignGenerator)
    gen.model = None
    gen.tokenizer = None

    # Load catalog manually
    catalog_path = os.path.join(
        os.path.dirname(__file__), "data/materials_catalog.json"
    )

    with open(catalog_path, "r") as f:
        gen.catalog = json.load(f)

    # Test get_available_options
    options = gen.get_available_options()

    print(f"✓ Available styles: {len(options['styles'])}")
    print(f"  {', '.join(options['styles'])}")

    print(f"✓ Available spaces: {len(options['spaces'])}")
    print(f"  {', '.join(options['spaces'])}")

    print(f"✓ Available sizes: {len(options['sizes'])}")
    print(f"  {', '.join(options['sizes'])}")

    # Test fallback generation
    print("\nTesting fallback generation...")
    spec = gen._fallback_generation(
        style="rustic",
        space="facade",
        size="medium",
        colors=["grey", "beige"],
        context=gen._build_context(
            gen.catalog["styles"]["rustic"],
            gen.catalog["spaces"]["facade"],
            gen.catalog["sizes"]["medium"],
        ),
    )

    print(f"✓ Generated fallback spec: {len(spec)} characters")
    print(f"✓ First 200 chars:\n{spec[:200]}...")

    print("\n✅ All structure tests PASSED")
    print("\nNote: Model loading test skipped (requires ~1GB download)")
    print(
        "To test full functionality, run: python main.py --style rustic --space facade --size medium --colors grey,beige --no-render"
    )


if __name__ == "__main__":
    test_structure()

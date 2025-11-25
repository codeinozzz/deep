import argparse
import os
from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator

def main():
    parser = argparse.ArgumentParser(description='AI Cladding & Facade Designer - Complete Generator')

    parser.add_argument('--style', type=str, required=True,
                       choices=['rustic', 'brutalism', 'minimalist', 'industrial',
                               'modern', 'mediterranean', 'scandinavian', 'contemporary_luxury'],
                       help='Architectural style')

    parser.add_argument('--space', type=str, required=True,
                       choices=['facade', 'living_room', 'kitchen', 'bathroom', 'bedroom',
                               'office', 'restaurant', 'store'],
                       help='Space type')

    parser.add_argument('--size', type=str, required=True,
                       choices=['small', 'medium', 'large'],
                       help='Space size')

    parser.add_argument('--colors', type=str, required=True,
                       help='Color palette separated by comma (e.g.: grey,beige)')

    parser.add_argument('--no-render', action='store_true',
                       help='Generate only specification without render')

    parser.add_argument('--output-dir', type=str, default='outputs',
                       help='Base directory for outputs')

    parser.add_argument('--steps', type=int, default=50,
                       help='Inference steps for Stable Diffusion (default: 50)')

    parser.add_argument('--guidance', type=float, default=7.5,
                       help='Guidance scale for Stable Diffusion (default: 7.5)')

    args = parser.parse_args()

    colors_list = [c.strip() for c in args.colors.split(',')]

    print("="*80)
    print("AI CLADDING & FACADE DESIGNER")
    print("="*80)
    print(f"\nConfiguration:")
    print(f"  Style: {args.style}")
    print(f"  Space: {args.space}")
    print(f"  Size: {args.size}")
    print(f"  Colors: {colors_list}")
    print("\n" + "="*80)

    print("\n[PHASE 1/2] Generating technical specification...")
    print("-"*80)

    design_gen = DesignGenerator()

    specification = design_gen.generate_specification(
        style=args.style,
        space=args.space,
        size=args.size,
        colors=colors_list
    )

    spec_dir = os.path.join(args.output_dir, 'specifications')
    os.makedirs(spec_dir, exist_ok=True)

    spec_filename = f"{args.style}_{args.space}_{args.size}.txt"
    spec_path = os.path.join(spec_dir, spec_filename)

    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(specification)

    print(f"\nSpecification saved: {spec_path}")
    print("\nPREVIEW:")
    print("-"*80)
    print(specification[:500] + "...")
    print("-"*80)

    if not args.no_render:
        print("\n[PHASE 2/2] Generating photorealistic render...")
        print("-"*80)

        render_gen = RenderGenerator()

        render_dir = os.path.join(args.output_dir, 'renders')

        image, render_path = render_gen.generate_render(
            style=args.style,
            space=args.space,
            specification=specification,
            colors=colors_list,
            output_dir=render_dir,
            filename=f"{args.style}_{args.space}_{args.size}.png",
            num_inference_steps=args.steps,
            guidance_scale=args.guidance
        )

        print(f"\nRender saved: {render_path}")
        print(f"Resolution: {image.size[0]}x{image.size[1]}")

    print("\n" + "="*80)
    print("GENERATION COMPLETED")
    print("="*80)
    print(f"\nResults:")
    print(f"  Specification: {spec_path}")
    if not args.no_render:
        print(f"  Render: {render_path}")
    print("\n")

if __name__ == "__main__":
    main()

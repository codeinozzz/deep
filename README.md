# AI Cladding & Facade Designer

AI-powered architectural cladding and facade design assistant that generates technical specifications and photorealistic visualizations.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-compatible GPU for faster processing

### Setup

1. Clone the repository or navigate to the project directory:
```bash
cd capstone-deep/cladding_designer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

### Quick Start

Run the test suite with 8 predefined design scenarios:
```bash
python test_designs.py
```

This will generate specifications for various combinations of styles, spaces, and sizes. Results are saved in `outputs/specifications/`.

### Custom Design Generation

Create a Python script or use the interactive Python shell:

```python
from models.design_generator import DesignGenerator

# Initialize the generator
generator = DesignGenerator()

# Generate a custom specification
specification = generator.generate_specification(
    style="rustic",
    space="facade",
    size="medium",
    colors=["grey", "beige"]
)

print(specification)
```

### Complete Pipeline (Specification + Render)

Generate both technical specification and photorealistic render:

```bash
# Rustic facade
python main.py --style rustic --space facade --size medium --colors "grey,beige"

# Brutalist living room
python main.py --style brutalism --space living_room --size small --colors "grey"

# Minimalist kitchen
python main.py --style minimalist --space kitchen --size medium --colors "white,light wood"

# Industrial office
python main.py --style industrial --space office --size large --colors "grey,black,brick"
```

### Test Complete System

Run full pipeline test with 5 design scenarios:

```bash
python test_renders.py
```

This generates both specifications and renders for multiple design combinations.

### Command Line Options

```bash
python main.py --help

Options:
  --style          Architectural style (required)
  --space          Space type (required)
  --size           Space size (required)
  --colors         Color palette, comma-separated (required)
  --no-render      Generate only specification, skip rendering
  --output-dir     Base directory for outputs (default: outputs)
  --steps          Inference steps for Stable Diffusion (default: 50)
  --guidance       Guidance scale for image generation (default: 7.5)
```

## Available Options

**Styles:**
- rustic (Rustic)
- brutalism (Brutalism)
- minimalist (Minimalist)
- industrial (Industrial)
- modern (Modern)
- mediterranean (Mediterranean)
- scandinavian (Scandinavian)
- contemporary_luxury (Contemporary Luxury)

**Spaces:**
- facade (Facade)
- living_room (Living room)
- kitchen (Kitchen)
- bathroom (Bathroom)
- bedroom (Bedroom)
- office (Office)
- restaurant (Restaurant)
- store (Store)

**Sizes:**
- small (Small < 20m²)
- medium (Medium 20-50m²)
- large (Large > 50m²)

## Project Structure

```
cladding_designer/
├── data/
│   └── materials_catalog.json    # Materials database
├── models/
│   ├── design_generator.py       # Text generation pipeline
│   └── render_generator.py       # Image generation pipeline
├── outputs/
│   ├── specifications/           # Generated specifications (.txt)
│   └── renders/                  # Generated renders (.png)
├── test_designs.py               # Test text generation only
├── test_renders.py               # Test complete pipeline
├── main.py                       # Main CLI integration
└── requirements.txt              # Python dependencies
```

## Usage Examples

### Example 1: Rustic Facade (Complete)
```bash
python main.py --style rustic --space facade --size medium --colors "grey,beige"
```
**Output:**
- Specification: `outputs/specifications/rustic_facade_medium.txt`
- Render: `outputs/renders/rustic_facade_medium.png`
- Materials: Natural stone, weathered wood, textured stucco
- Color palette: Grey stone, beige sand, wood accents

### Example 2: Brutalist Living Room
```bash
python main.py --style brutalism --space living_room --size small --colors "grey"
```
**Output:**
- Specification with exposed concrete, polished flooring, industrial accents
- Photorealistic render with dramatic lighting and raw materials

### Example 3: Minimalist Kitchen
```bash
python main.py --style minimalist --space kitchen --size medium --colors "white,light wood"
```
**Output:**
- White porcelain tiles, light wood details, clean lines
- High-quality architectural visualization

### Example 4: Text Generation Only
```bash
python main.py --style mediterranean --space facade --size large --colors "white,terracotta" --no-render
```
Generates only the technical specification without creating the render (faster for planning).

## Application Design & Architecture

### System Overview

The AI Cladding & Facade Designer is built as a two-stage pipeline that transforms user requirements into detailed architectural specifications and photorealistic visualizations.

```
User Input → Text Generation → Image Generation → Final Output
  (Style,      (Specification)   (Photorealistic   (Spec +
   Space,                          Render)          Render)
   Size)
```

### Architecture Components

#### 1. Data Layer (`data/`)
- **materials_catalog.json**: Comprehensive database of cladding materials with properties:
  - Material names and categories (wood, concrete, metal, etc.)
  - Physical properties (dimensions, finishes, textures)
  - Aesthetic attributes (colors, patterns)
  - Application contexts (exterior facades, interior walls, etc.)

#### 2. Text Generation Pipeline (`models/design_generator.py`)
- **Purpose**: Generate detailed technical specifications from user parameters
- **Technology**: Pre-trained language model (transformers)
- **Process**:
  1. Accepts user input (style, space, size, colors)
  2. Queries materials catalog for appropriate materials
  3. Generates structured specification including:
     - Material recommendations
     - Layout patterns
     - Installation guidelines
     - Technical requirements
- **Output**: Text-based specification file saved to `outputs/specifications/`

#### 3. Image Generation Pipeline (`models/render_generator.py`)
- **Purpose**: Create photorealistic renders from specifications
- **Technology**: Stable Diffusion model
- **Process**:
  1. Reads generated specification
  2. Constructs optimized prompt for image model
  3. Generates high-quality architectural visualization
  4. Post-processes image for consistency
- **Output**: Image file saved to `outputs/renders/`

### Data Flow

```
┌─────────────────┐
│   User Input    │
│  (Parameters)   │
└────────┬────────┘
         │
         v
┌─────────────────────────┐
│  Design Generator       │
│  - Load materials DB    │
│  - Filter by criteria   │
│  - Generate spec        │
└────────┬────────────────┘
         │
         v
┌─────────────────────────┐
│  Specification File     │
│  (.txt in outputs/)     │
└────────┬────────────────┘
         │
         v
┌─────────────────────────┐
│  Render Generator       │
│  - Parse specification  │
│  - Create prompt        │
│  - Generate image       │
└────────┬────────────────┘
         │
         v
┌─────────────────────────┐
│  Photorealistic Render  │
│  (.png in outputs/)     │
└─────────────────────────┘
```

### Design Decisions

1. **Modular Pipeline**: Separate text and image generation allows independent development and testing
2. **Catalog-Based Approach**: Materials database ensures realistic, buildable specifications
3. **Structured Outputs**: Standardized file formats enable easy integration with external tools
4. **Extensible Options**: Style/space/size parameters can be expanded without core changes

### Technology Stack

- **Language**: Python 3.8+
- **AI/ML Frameworks**:
  - PyTorch: Deep learning foundation
  - Transformers: Pre-trained language models
  - Diffusers: Stable Diffusion image generation
  - Accelerate: Model optimization
- **Data Processing**: NumPy, JSON
- **Image Processing**: Pillow (PIL)
- **Storage**: File-based outputs (specifications as .txt, renders as .png)

### Development Roadmap

**Week 1-2**: Text Generation Pipeline
- Material catalog design
- Specification generator implementation
- Test suite with 8 scenarios
- Status: ✅ Completed

**Week 3-4**: Image Generation Pipeline
- Stable Diffusion integration
- Prompt engineering for architectural renders
- Image quality optimization
- Full pipeline integration with main.py
- CLI interface with argparse
- Status: ✅ Completed

**Future Enhancements**:
- Web interface for easier user interaction
- 3D model generation
- Cost estimation based on materials
- Interactive material customization
- Multi-language support (English, Spanish)

### Output Examples

**Specification Output** (`outputs/specifications/`):
```
Cladding for Rustic Style Facade (Medium: 20-50m²)

Primary Materials:
- Weathered Wood: Pine or oak planks with natural finish...
- Natural Stone: Limestone decorative elements...

Installation Pattern: Horizontal with irregular joints...
```

**Render Output** (`outputs/renders/`):
- High-resolution photorealistic architectural visualization
- Accurate material representation
- Contextual environment and lighting

## Performance Notes

### Hardware Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 10GB free space
- Generation time: 3-5 minutes per render (CPU)

**Recommended:**
- GPU: NVIDIA with 6GB+ VRAM (CUDA support)
- RAM: 16GB
- Disk: 20GB free space
- Generation time: 30-60 seconds per render (GPU)

### Optimization Tips

1. **First run downloads models** (~5GB for Stable Diffusion)
2. **Use GPU when available** - automatic detection enabled
3. **Adjust inference steps** for speed/quality tradeoff:
   - Fast: `--steps 20` (lower quality)
   - Balanced: `--steps 50` (default)
   - High quality: `--steps 100` (slower)
4. **Skip rendering for planning** - use `--no-render` flag
5. **Batch processing** - use `test_renders.py` for multiple designs

### Troubleshooting

**Out of memory error:**
```bash
# Reduce inference steps
python main.py --style rustic --space facade --size medium --colors "grey" --steps 20
```

**Slow generation:**
- Ensure CUDA is properly installed for GPU acceleration
- First run is slower due to model downloads
- Subsequent runs use cached models

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Authentication error with Hugging Face:**
If you see a 401 error when loading the Stable Diffusion model:
```bash
# Option 1: Install and login to Hugging Face CLI
pip install huggingface_hub
huggingface-cli login

# Then accept terms at: https://huggingface.co/runwayml/stable-diffusion-v1-5
```

The project uses `runwayml/stable-diffusion-v1-5` by default, which has fewer restrictions than other models.

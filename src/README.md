# AI Cladding & Facade Designer

AI-powered architectural cladding and facade design assistant that generates technical specifications and photorealistic visualizations using deep learning models.

## Overview

This project uses:
- **Text Generation**: FLAN-T5-base (Hugging Face) for architectural specifications
- **Image Generation**: Stable Diffusion v1.5 for photorealistic renders
- **No paid APIs required** - fully open-source solution

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4-8GB RAM minimum (CPU mode)
- (Optional) CUDA-compatible GPU for faster processing

### Setup

1. Navigate to the project source directory:
```bash
cd src
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

4. Install PyTorch (choose based on your system):
```bash
# CPU only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision
```

5. Install remaining dependencies:
```bash
pip install transformers diffusers accelerate pillow
```

### First Run Setup

On first run, the system will automatically download required models:
- FLAN-T5-base (~1GB) - for text generation
- Stable Diffusion v1.5 (~5GB) - for image generation

This may take 10-20 minutes depending on your internet connection.
Models are cached locally and reused for subsequent runs.

## How to Run

### Quick Start - Text Generation Only

Test the text generation system:
```bash
python test_designs.py
```

This will generate specifications for various design scenarios using FLAN-T5-base.
Results are saved in `outputs/specifications/`.

### Complete Pipeline (Specification + Render)

Generate both technical specification and photorealistic render:

```bash
# Basic usage
python main.py --style rustic --space facade --size medium --colors "grey,beige"

# More examples
python main.py --style brutalism --space living_room --size small --colors "grey"
python main.py --style minimalist --space kitchen --size medium --colors "white,beige"
python main.py --style industrial --space facade --size large --colors "grey,black"
```

### Generate Specification Only (Faster)

Skip image generation to test text generation only:
```bash
python main.py --style rustic --space facade --size medium --colors "grey,beige" --no-render
```

### Custom Integration

Use the generator in your own Python code:

```python
from models.design_generator import DesignGenerator

# Initialize the generator (loads FLAN-T5-base)
generator = DesignGenerator()

# Generate specification
specification = generator.generate_specification(
    style="rustic",
    space="facade",
    size="medium",
    colors=["grey", "beige"]
)

print(specification)
```

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

The AI Cladding & Facade Designer is built as a two-stage pipeline that transforms user requirements into detailed architectural specifications and photorealistic visualizations using open-source deep learning models.

```
User Input → Text Generation → Image Generation → Final Output
  (Style,      (FLAN-T5-base)    (Stable          (Spec +
   Space,                          Diffusion)      Render)
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
- **Technology**: FLAN-T5-base (Google, via Hugging Face)
- **Model Details**:
  - Encoder-decoder transformer architecture
  - Fine-tuned on instruction-following tasks
  - ~250M parameters
  - No API key required
- **Process**:
  1. Accepts user input (style, space, size, colors)
  2. Queries materials catalog for appropriate materials
  3. Uses FLAN-T5 to generate each specification section:
     - Project overview and design philosophy
     - Material recommendations with descriptions
     - Color palette strategy
     - Installation patterns and techniques
     - Technical requirements
     - Budget estimation
  4. Falls back to template generation if model fails
- **Output**: Text-based specification file saved to `outputs/specifications/`
- **Performance**: 30-60 seconds on CPU, 5-10 seconds on GPU

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
- **Deep Learning Models**:
  - FLAN-T5-base: Text generation (google/flan-t5-base)
  - Stable Diffusion v1.5: Image generation (runwayml/stable-diffusion-v1-5)
- **AI/ML Frameworks**:
  - PyTorch: Deep learning foundation
  - Transformers (Hugging Face): Model loading and inference
  - Diffusers: Stable Diffusion pipeline
  - Accelerate: Model optimization
- **Data Processing**: JSON-based material catalog
- **Image Processing**: Pillow (PIL)
- **Storage**: File-based outputs (specifications as .txt, renders as .png)
- **Cost**: 100% free, no API keys or subscriptions required

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

**Minimum (CPU-only):**
- CPU: 4 cores
- RAM: 4-8GB
- Disk: 10GB free space (6GB for models, rest for outputs)
- Generation time:
  - Text: 30-60 seconds
  - Image: 2-4 minutes
  - Total: ~3-5 minutes per complete design

**Recommended (with GPU):**
- GPU: NVIDIA with 6GB+ VRAM (CUDA support)
- RAM: 8-16GB
- Disk: 15GB free space
- Generation time:
  - Text: 5-10 seconds
  - Image: 30-60 seconds
  - Total: ~1 minute per complete design

### Optimization Tips

1. **First run downloads models** (~6GB total: 1GB FLAN-T5 + 5GB Stable Diffusion)
   - Models are cached in `~/.cache/huggingface/`
   - Subsequent runs are much faster
2. **Use GPU when available** - automatic detection enabled
3. **Adjust inference steps** for image quality vs speed:
   - Fast: `--steps 20` (lower quality, ~1 min on CPU)
   - Balanced: `--steps 50` (default, ~3 min on CPU)
   - High quality: `--steps 100` (slower, ~5 min on CPU)
4. **Skip rendering for planning** - use `--no-render` flag for text-only
5. **CPU optimization**:
   - Close other applications to free RAM
   - FLAN-T5-base is optimized for CPU inference
   - Consider using `--steps 20` for faster iterations

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
pip install --upgrade torch transformers diffusers accelerate pillow
```

**Model download fails:**
```bash
# Manually download models
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('google/flan-t5-base')"
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

**Hugging Face access (if needed):**
Both FLAN-T5-base and Stable Diffusion v1.5 are publicly available and don't require authentication. If you encounter access issues:
```bash
pip install huggingface_hub
huggingface-cli login
```

**Slow text generation:**
- FLAN-T5 generates text section by section (6 sections total)
- Each section takes 5-10 seconds on CPU
- This is normal for local model inference
- Consider using GPU for faster generation

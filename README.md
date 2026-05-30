<div align="center">

# Boolbox

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status: Development](https://img.shields.io/badge/status-development-orange.svg)

<br>
</div>

A lightweight cryptographic Boolean function analysis and quantum circuit synthesis tool and library. It helps you analyze cryptographic Substitution Boxes (S-Boxes) by computing their Algebraic Normal Form (ANF) polynomials, truth tables, and Möbius transform coefficients, as well as synthesizing quantum circuits representing those equations.

## Features

* **ANF Equation Generation**: Generate Algebraic Normal Form (ANF) equations for each S-Box bit.
* **Truth Tables**: Extract individual truth tables for output bits.
* **Möbius Coefficients**: Compute Fast Möbius Transform (FMT) coefficients.
* **Quantum Circuit Synthesis**: Synthesize out-of-place quantum circuits (reversible logic) directly from the generated ANF polynomials.
* **Flexible Input**: Load S-Boxes from raw strings, local files, or standard input (stdin).

## Formatters

The tool supports multiple output formats for ANF equations:

* **Text (`text`)**: Standard text representation of equations.
* **LaTeX (`latex`)**: Outputs mathematical equations formatted with standard LaTeX symbols.
* **JSON (`json`)**: Structured data format containing equations and metadata, useful for integration with other tools.
* **Unicode (`unicode`)**: Visually formatted text utilizing subscript numbers and mathematical symbols (e.g., `⊕`, `→`).
* **Image (`image`)**: Renders and saves equations to a PNG image file using `matplotlib`.

## Installation

### From Source (Development)
Clone the repository and install the package with editable mode. You can choose the extras configuration depending on your use case:

```bash
git clone https://github.com/cysctl/boolbox.git
cd boolbox

# Core package with basic image export
pip install -e .[image]

# Basic quantum circuit synthesis (Qiskit support)
pip install -e .[quantum]

# Quantum circuit synthesis with visualization capabilities (Matplotlib & pylatexenc)
pip install -e .[quantum-vis]

# Complete installation with all features and development dependencies (pytest)
pip install -e .[all,dev]
```

Verify your installation with:
```bash
boolbox --help
```

### From PyPI (Coming Soon)
`boolbox` will soon be available on PyPI. Once published, you will be able to install it directly using pip:

```bash
pip install boolbox
```

## Usage

Once installed, the `boolbox` command is available globally.

### 1. Generate ANF Equations (`anf`)
Convert S-Box outputs to algebraic equations.

```bash
# Standard text format (default)
boolbox anf "[0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]"

# Unicode format
boolbox anf "[0xC, 0x5, 0x6, 0xB]" --format unicode

# LaTeX format
boolbox anf "[0xC, 0x5, 0x6, 0xB]" --format latex

# Save equations as a PNG image (requires 'matplotlib')
boolbox anf "[0xC, 0x5, 0x6, 0xB]" --format image --output equations.png
```

### 2. Extract Truth Tables (`tts`)
Extract truth tables for each S-Box output bit.

```bash
boolbox tts "[0xC, 0x5, 0x6, 0xB]" --format json
```

### 3. Generate Möbius Coefficients (`coeffs`)
Compute Fast Möbius Transform coefficients.

```bash
boolbox coeffs "[0xC, 0x5, 0x6, 0xB]" --format text
```

### 4. Synthesize Quantum Circuits (`qcircuit`)
Synthesize a Qiskit-compatible quantum circuit from an S-Box ANF.

```bash
# Display circuit structure as ASCII/Text directly on stdout (default)
boolbox qcircuit "[0xC, 0x5, 0x6, 0xB]"

# Export ASCII circuit rendering to a text file
boolbox qcircuit "[0xC, 0x5, 0x6, 0xB]" --format text --output circuit.txt

# Render and save the circuit as an MPL-based PNG image (requires 'quantum-vis' extras)
boolbox qcircuit "[0xC, 0x5, 0x6, 0xB]" --format image --output quantum_circuit.png
```
> **Note:** As `boolbox` is primarily designed for educational and learning purposes, the synthesized circuits are intended for demonstration and baseline functionality, rather than representing optimal or physically simplified quantum layouts.

### Input Methods
Inputs can be supplied through different channels:
```bash
# Read from a file
boolbox anf path/to/sbox.txt

# Pipe from standard input (stdin)
cat sbox.txt | boolbox anf -
```

## Roadmap

Planned improvements and features for future releases:

- **Expand LaTeX Formatting Support:** Extend LaTeX output support to the remaining subcommands (`tts` and `coeffs`), where it is currently pending implementation.
- **Universal Output Routing:** Extend the `-o/--output` flag functionality to support all formatters (Text, JSON, LaTeX, etc.), allowing users to write any generated output directly to a file instead of `stdout`.
- **Formatter Architecture Refactoring:** Introduce dedicated formatter families for Truth Tables (`TruthTableFormatter`) and Möbius Coefficients (`CoeffsFormatter`). This architectural upgrade will eliminate inline `if/elif` conditional logic, enforcing a cleaner and fully polymorphic design across all subcommands.

## AI Usage Policy

This project was developed with assistance from Artificial Intelligence. AI tools were utilized for the following tasks:
* Optimizing the Fast Möbius Transform algorithm to reduce its complexity.
* Drafting and formatting this `README.md` file.
* Minor refactoring and routine code adjustments.

The core design, structural logic, program architecture, and implementation are designed and owned by the author.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
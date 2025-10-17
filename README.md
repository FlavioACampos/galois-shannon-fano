# Galois Fields and Shannon-Fano Coding

This project implements the Shannon-Fano coding algorithm combined with Galois Fields for error detection and correction. It provides a practical demonstration of information theory and finite field mathematics.

## Features

- Shannon-Fano prefix code generation
- Character frequency analysis
- Galois Field construction (GF(2ⁿ))
- Error detection and correction
- Visualization tools
- Interactive Jupyter notebook demos

## Requirements

- Python 3.7 or higher
- Dependencies:
  - NumPy (≥ 1.19.0)
  - Pandas (≥ 1.0.0)
  - Matplotlib (≥ 3.3.0)
  - NetworkX (≥ 2.5)
  - Jupyter (≥ 1.0.0)

## Installation

```bash
pip install -e .
```

## Usage

The package provides both a command-line interface and a Python API. See the Jupyter notebook `examples/demo.ipynb` for interactive examples.

Basic usage:

```python
from io import StringIO
from src.shannon_fano import string_frequencies, shannon_fano
from src.galois_field import field_constructor
from src.binary_utils import string_to_binary, binary_errors

# Encode a string
text = "Hello, World!"
freqs, chars, _ = string_frequencies(text)
codes = shannon_fano(freqs, chars)

# Convert to binary
binary = string_to_binary(text)

# Introduce some errors
corrupted = binary_errors(binary)

# Create Galois Field
output = StringIO()
field_constructor(4, output)  # Creates GF(2⁴)

# Access the field data
output.seek(0)  # Reset buffer position
field_data = output.read()  # Get the CSV content
print(field_data)  # Or save to file/process the data
```

## Interactive Demo

The project includes a comprehensive Jupyter notebook (`examples/demo.ipynb`) that demonstrates:

1. Text encoding using Shannon-Fano coding
2. Visualization of encoding trees
3. Galois Field construction and properties
4. Error detection and correction examples
5. Performance analysis

To run the demo:

```bash
jupyter notebook examples/demo.ipynb
```

## Theory

### Shannon-Fano Coding

Shannon-Fano coding is a technique for constructing a prefix code based on a set of symbols and their probabilities. It works by recursively dividing the symbols into groups to create optimal binary codes.

### Galois Fields

A Galois Field GF(2ⁿ) is a finite field with 2ⁿ elements. These fields are essential in error-correcting codes as they provide the mathematical foundation for detecting and correcting bit errors.

## Project Structure

```
galois-shannon-fano/
├── src/
│   ├── __init__.py
│   ├── shannon_fano.py  # Shannon-Fano coding implementation
│   ├── galois_field.py  # Galois Field operations
│   ├── binary_utils.py  # Binary conversion utilities
│   ├── core.py         # Common utilities
│   └── data/
│       └── polynomials.json  # Pre-computed polynomials
├── examples/
│   └── demo.ipynb      # Interactive demonstrations
├── tests/              # Unit tests
├── setup.py           # Package configuration
└── README.md          # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

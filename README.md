# Galois Fields and Shannon-Fano Coding

This project implements the Shannon-Fano coding algorithm combined with Galois Fields for error detection and correction. It provides a practical demonstration of information theory and finite field mathematics.

## Features

- Shannon-Fano prefix code generation
- Character frequency analysis
- Galois Field construction (GF(2ⁿ))
- Error detection and correction
- Visualization tools
- Interactive Jupyter notebook demos

## Installation

```bash
pip install -e .
```

## Usage

The package provides both a command-line interface and a Python API. See the Jupyter notebook `demo.ipynb` for interactive examples.

Basic usage:

```python
from shannon_fano import shannon_fano
from galois_field import field_constructor
from binary_utils import string_to_binary, binary_errors

# Encode a string
text = "Hello, World!"
freqs, chars = get_frequencies(text)
codes = shannon_fano(freqs, chars)

# Convert to binary
binary = string_to_binary(text)

# Introduce some errors
corrupted = binary_errors(binary)

# Create Galois Field
field = field_constructor(4)  # Creates GF(2⁴)
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
│   ├── shannon_fano.py
│   ├── galois_field.py
│   ├── binary_utils.py
│   └── polynomials.py
├── tests/
├── demo.ipynb
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

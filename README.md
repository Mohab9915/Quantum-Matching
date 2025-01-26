# BioMesh: Quantum Plant-Microbe Matching System 🌿🔬

A sophisticated application that uses quantum computing principles to optimize plant-microbe pairings for enhanced agricultural outcomes.

## Overview

BioMesh leverages both quantum (QAOA) and classical algorithms to identify optimal plant-microbe combinations based on their traits and environmental conditions. The system uses Qiskit for quantum computations and Streamlit for the user interface.

## Features

- 🔄 Dual Algorithm Support: Choose between Quantum and Classical matching
- 🎯 Trait-based Compatibility Scoring
- 📊 Interactive Data Visualization
- ⚡ Real-time Performance Metrics
- 🔮 Futuristic Simulation Mode

## How It Works

1. **Data Input**
   - Upload CSV files containing plant and microbe characteristics
   - Plants data must include: Name, Root Depth, Drought Resistance, Optimal Condition
   - Microbes data must include: Name, Nitrogen Fixation, Salt Tolerance, Optimal Condition

2. **Algorithm Selection**
   - **Quantum Mode**: Uses QAOA to find optimal trait combinations
   - **Classical Mode**: Uses direct trait matching based on user preferences

3. **Trait Matching**
   - Evaluates compatibility based on:
     - Root depth compatibility
     - Drought resistance levels
     - Nitrogen fixation capability
     - Salt tolerance
     - Environmental conditions

4. **Output**
   - Displays ranked pairs of plants and microbes
   - Shows compatibility scores (0-100%)
   - Provides detailed quantum specifications when applicable

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/biomesh.git

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the Streamlit app
streamlit run app.py
```

## Requirements

- Python 3.8+
- Qiskit
- Streamlit
- Pandas
- NumPy

## Data Format

### plants.csv
```csv
Name,Root Depth,Drought Resistance,Optimal Condition
Plant1,deep,high,arid
Plant2,shallow,low,tropical
```

### microbes.csv
```csv
Name,Nitrogen Fixation,Salt Tolerance,Optimal Condition
Microbe1,high,high,arid
Microbe2,low,moderate,tropical
```

## Configuration Options

- **QAOA Iterations**: Control quantum algorithm precision (50-500)
- **QAOA Layers**: Adjust quantum circuit depth (1-5)
- **Simulation Type**: Choose between realistic and futuristic timing modes
- **Algorithm Parameters**: Customize trait targeting preferences

## Technical Details

The quantum implementation uses:
- QAOA (Quantum Approximate Optimization Algorithm)
- Custom Hamiltonians for plant and microbe trait optimization
- SparsePauliOp for quantum state representation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# **Photosynthesis Simulation Project

# Overview**
This repository contains a Python implementation to model a simplified version of the photosynthesis process. The project is divided into three main classes: Atom, Molecule, and Chloroplast. Each class represents a fundamental component of the photosynthesis process and works together to simulate how plants convert light energy into chemical energy. This implementation demonstrates basic object-oriented programming principles, including class design, method implementation, and interaction between objects.

**Purpose**
The purpose of this assignment is to develop a functional simulation of the photosynthesis process, encompassing the following:

Atom Representation: Modeling individual atoms with properties such as symbol, atomic number, and neutrons, and providing functionality for isotope representation and comparison.

Molecule Representation: Creating molecules from atoms, representing them in a human-readable format, and allowing for the combination of molecules.

Chloroplast Simulation: Simulating the photosynthesis process by managing water and CO2 molecules and performing photosynthesis when sufficient quantities are present.

# Methodology
### 1. Atom Class
Initialization: Represents an atom with a symbol, atomic number, and neutrons.
Methods:
proton_number(): Returns the number of protons.
mass_number(): Returns the atom's mass number (sum of protons and neutrons).
isotope(neutrons): Updates the number of neutrons for the atom.
Comparison Methods: Implements comparison operations for isotopes of the same element.
## 2. Molecule Class
Initialization: Represents a molecule as a collection of atoms.
Methods:
__str__(): Provides a string representation of the molecule in chemical formula format.
__add__(other): Allows for the addition of two molecules to create a new molecule.
## 3. Chloroplast Class
Initialization: Manages water and CO2 molecules.
Methods:
add_molecule(molecule): Adds a molecule to the chloroplast and performs photosynthesis if conditions are met.
__str__(): Provides a string representation of the chloroplast's current state.
Data Process
Atom Class Testing:
Tests include creating various isotopes and comparing them based on mass number.
Molecule Class Testing:
Tests include creating and printing molecules, and adding molecules together.
Chloroplast Class Testing:
Tests include adding water and CO2 molecules and simulating photosynthesis.

# Files:
Atom_class.py: Contains the Atom class definition.
molecule_class.py: Contains the Molecule class definition.
chloroplast_class.py: Contains the Chloroplast class definition.
test_script.py: Contains test cases for Atom, Molecule, and Chloroplast classes.
README.md: This file.

# How to use:
-Clone the Repository.
-Navigate to the Project Directory.
-Run the classes files including tests.


Author
F. Monfared f.monfared@st.hanze.nl
  
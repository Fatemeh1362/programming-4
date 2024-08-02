
from Atom_class import Atom
class Molecule:
    def __init__(self, atoms):
        """
        Initializing a Molecule object.

        Parameters:
        atoms (list of tuples): Each tuple contains an Atom object and the number of atoms of that type.
        """
        if not all(isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], Atom) and isinstance(item[1], int) for item in atoms):
            raise ValueError("Each element in the atoms list must be a tuple of Atom and int.")
        
        self.atoms = atoms  # storingthe list of (Atom, count) tuples

    def __str__(self):
        """
        returning a string representation of the Molecule object.

        Returns:
        str: A string representing the molecule in a chemical formula format.
        """
        formula_parts = []
        for atom, count in self.atoms:
            if count > 1:
                formula_parts.append(f"{atom.symbol}{count}")
            else:
                formula_parts.append(f"{atom.symbol}")
        return ''.join(formula_parts)

    def __add__(self, other):
        """
        Adding two Molecule objects together.
        Parameters:
        other (Molecule)The other molecule to add.

        Returns:
        Molecule: A new Molecule object representing the combined molecules.

        Raises:
        TypeError: If the other object is not a Molecule.
        """
        if not isinstance(other, Molecule):
            raise TypeError("Can only add Molecule to Molecule.")

        # Combine atoms from both molecules
        combined_atoms = {}
        for atom, count in self.atoms:
            if atom.symbol in combined_atoms:
                combined_atoms[atom.symbol] += count
            else:
                combined_atoms[atom.symbol] = count

        for atom, count in other.atoms:
            if atom.symbol in combined_atoms:
                combined_atoms[atom.symbol] += count
            else:
                combined_atoms[atom.symbol] = count

        # Creating Atom instances based on the combined atom symbols
        combined_atoms_list = [(self._create_atom(symbol), count) for symbol, count in combined_atoms.items()]

        return Molecule(combined_atoms_list)

    def _create_atom(self, symbol):
        """
        create an Atom object with the given symbol. This is a helper function to create Atom instances.

        Parameters:
        symbol (str): The symbol of the atom to create.

        Returns:
        Atom: The Atom object with the given symbol.

        Raises:
        ValueError: If no Atom with the given symbol is found.
        """
        # Define atomic numbers and neutrons for simplicity
        atomic_data = {
            'H': (1, 0),
            'C': (6, 6),
            'O': (8, 8)
            # Adding more elements if necessary
        }

        if symbol in atomic_data:
            atomic_number, neutrons = atomic_data[symbol]
            return Atom(symbol, atomic_number, neutrons)
        else:
            raise ValueError(f"Atom with symbol {symbol} not found.")



# Creating Atom instances
hydrogen = Atom('H', 1, 0)
carbon = Atom('C', 6, 6)
oxygen = Atom('O', 8, 8)

# Creating Molecule instances
water = Molecule([(hydrogen, 2), (oxygen, 1)])
co2 = Molecule([(carbon, 1), (oxygen, 2)])

# Test __str__ method
print(water)  # Expected Output: H2O
print(co2)    # Expected Output: CO2

# Test __add__ method
combined_molecule = water + co2
print(combined_molecule)  # Expected Output: H2OCO2

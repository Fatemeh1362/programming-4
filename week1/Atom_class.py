class Atom:
    def __init__(self, symbol, atomic_number, neutrons):
        """
        Initializing an Atom instance.

        Parameters:
        symbol (str): the chemical symbol of the atom (e.g., 'H', 'O').
        atomic_number (int): The atomic number (number of protons) of the atom.
        neutrons (int): The number of neutrons in the atom.
        """
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.neutrons = neutrons

    def proton_number(self):
        """
        returning the number of protons in the atom, which is the atomic number.

        returns:
        int:the atomic number of the atom.
        """
        return self.atomic_number

    def mass_number(self):
        """
        returning the mass number of the atom, which is the sum of protons and neutrons.

        returns:
        int: The mass number of the atom.
        """
        return self.atomic_number + self.neutrons

    def with_isotope(self,neutrons):
        """
        Create a new Atom instance with a different number of neutrons.

        Parameters:
        neutrons (int): The new number of neutrons for the isotope.

        Returns:
        Atom: A new Atom instance with the updated neutron count.
        """
        return Atom(self.symbol, self.atomic_number, neutrons)

    def __eq__(self,other):
        """
        Check if two Atom instances are equal.
        Parameters:
        other (Atom): The other Atom instance to compare.

        Returns:
        bool: True if the atoms have the same symbol and mass number, False otherwise.
        """
        if not isinstance(other, Atom):
            return False
        return self.symbol == other.symbol and self.mass_number() == other.mass_number()

    def __lt__(self,other):
        """
        Check if this Atom instance is less than another Atom instance.

        Parameters:
        other (Atom): The other Atom instance to compare.

        Returns:
        bool: True if this atom's mass number is less than the other atom's mass number.
        
        Raises:
        TypeError: If the other instance is not an Atom.
        ValueError: If the atoms are not of the same element.
        """
        if not isinstance(other,Atom):
            raise TypeError("Comparisons must be between Atom instances.")
        if self.symbol != other.symbol:
            raise ValueError("Comparisons must be between isotopes of the same element.")
        return self.mass_number() < other.mass_number()

    def __le__(self,other):
        """
        Checking if this Atom instance is less than or equal to another Atom instance.

        Parameters:
        other (Atom): The other Atom instance to compare.

        Returning:
        bool: True if this atom's mass number is less than or equal to the other atom's mass number.
        Raises:
        TypeError: If the other instance is not an Atom.
        ValueError: If the atoms are not of the same element.
        """
        if not isinstance(other, Atom):
            raise TypeError("Comparisons must be between Atom instances.")
        if self.symbol != other.symbol:
            raise ValueError("Comparisons must be between isotopes of the same element.")
        return self < other or self == other

    def __gt__(self, other):
        """
        Checking if this Atom instance is greater than another Atom instance.

        Parameters:
        other (Atom): The other Atom instance to compare.

        Returns:
        bool: True if this atom's mass number is greater than the other atom's mass number.
        Raises:
        TypeError: If the other instance is not an Atom.
        ValueError: If the atoms are not of the same element.
        """
        if not isinstance(other, Atom):
            raise TypeError("Comparisons must be between Atom instances.")
        if self.symbol != other.symbol:
            raise ValueError("Comparisons must be between isotopes of the same element.")
        return self.mass_number() > other.mass_number()

    def __ge__(self, other):
        """
        checkingif this Atom instance is greater than or equal to another Atom instance.

        Parameters:
        other (Atom): The other Atom instance to compare.

        Returns:
        bool: True if this atom's mass number is greater than or equal to the other atom's mass number.
        
        Raises:
        TypeError: If the other instance is not an Atom.
        ValueError:If the atoms are not of the same element.
        """
        if not isinstance(other, Atom):
            raise TypeError("Comparisons must be between Atom instances.")
        if self.symbol!= other.symbol:
            raise ValueError("Comparisons must be between isotopes of the same element.")
        return self >other or self == other

    def __repr__(self):
        """
        Return a string representation of the Atom instance.

        Returns:
        str:A string representation of the Atom.
        """
        return f"Atom(symbol={self.symbol}, atomic_number={self.atomic_number}, neutrons={self.neutrons})"

# Testing the Atom class
protium =Atom('H', 1,0)
deuterium = Atom('H', 1,1)
tritium = Atom('H', 1,2)

# Changingisotope
oxygen = Atom('O',8, 8)
oxygen_isotope = oxygen.with_isotope(10)  # Different isotope of Oxygen

# Assertions
assert tritium.neutrons == 2
assert tritium.mass_number() == 3
assert protium <deuterium
assert deuterium <= tritium
assert tritium >= protium

# Test comparisons between same elements
print(oxygen < oxygen_isotope)  #Should be True
print(oxygen > oxygen_isotope)  #Should be False

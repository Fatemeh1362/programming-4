from molcule_class import Molecule
from Atom_class import Atom

class Chloroplast:
    def __init__(self):
        """
        Initializing a Chloroplast object with water and CO2 counts set to 0.
        """
        self.water = 0
        self.co2 = 0

    def add_molecule(self,molecule):
        """
        adding a molecule to the chloroplast.
        Parameters:
        molecule (Molecule): The molecule to add(should be water or CO2).

        Returns:
        list:An empty list if no photosynthesis occurso therwise a list of tuples of new molecules.
        Raises:
        ValueError: If the molecule is neither water nor CO2.
        """
        # Checking the type of molecule to count the number of each molcule
        if str(molecule) == 'H2O':
            self.water += 1
        elif str(molecule) =='CO2':
            self.co2 += 1
        else:
            raise ValueError("Only H2O or CO2 molecules are allowed.")
        
        # Checking if we can perform photosynthesis
        if self.co2 >= 6 and self.water >= 12:
            self.co2 -= 6
            self.water -= 12

            # You should return a tuple of Molecules and numbers, not of strings and numbers.
            return [('C6H12O6',1), ('O2',6)]
        
        return []

    def __str__(self):
        """
        Return a string representation of the Chloroplast object.
        Returns:
        str:The current state of the chloroplast in terms of stored water and CO2 molecules.
        """
        return f"Chloroplast with {self.water} water molecules and {self.co2} CO2 molecules."

# Creating Atom instances
hydrogen = Atom('H', 1, 0)
carbon = Atom('C', 6, 6)
oxygen = Atom('O', 8, 8)

# Create Molecule instances to store water and co2 molcules
water = Molecule([(hydrogen, 2), (oxygen, 1)])
co2 = Molecule([(carbon, 1), (oxygen, 2)])

# Creating a Chloroplast instance
demo = Chloroplast()
els = [water, co2]

while True:
    print('\nWhat molecule would you like to add?')
    print('[1] Water')
    print('[2] Carbondioxide')
    print('Please enter your choice: ',end='')
    try:
        choice = int(input())
        if choice not in [1, 2]:
            raise ValueError("Choice must be 1 or 2.")
        res = demo.add_molecule(els[choice - 1])
        if len(res) == 0:
            print(demo)
        else:
            print('\n=== Photosynthesis!')
            print(res)
            print(demo)

    except Exception as e:
        print(f'\n=== That is not a valid choice. Error: {e}')

# HSRM Report Generation Project
# ## Overview
This repository contains a  project designed to generate reports from HealthShare Referral Manager (HSRM) files. In project some classes has been defined already by downloading them and and by using these classes as moduel we can extracts specific information (CCS information). We mainly focuse on the principles needed to be considered in defining classes to increase the readability and maintainbibity and extensive ability.

## Purpose
The purpose of this assignment is to perform static code analysis on the provided codebase. The tasks include understanding the general workings of the application, creating UML diagrams, evaluating adherence to SOLID principles, and providing recommendations for improvements.

## Methodology
Exercise 1: Workings
Objective: Understand the general workings of the application and create a sequence diagram.
Approach:
Start with main.py and trace the flow of the application.
Use an IDE like VS Code to navigate through the codebase.
Create a sequence diagram using a tool like PlantUML.

Exercise 2: The Factory
Objective: Understand the factory pattern used in the application and evaluate its adherence to the Interface Segregation Principle.
Approach:
Review the parserTypes.py file and the factory implementation.
Determine if the factory method adheres to the Interface Segregation Principle.

Exercise 3: Single Responsibility
Objective: Evaluate if the classes related to CCS classification adhere to the Single Responsibility Principle.
Approach:
Review the Python files starting with Ccs.
Determine if each class has a single responsibility.

Exercise 4: The Base Classes
Objective: Identify examples of the Liskov Substitution Principle in the code.
Approach:
Find base classes and their derived classes.
Determine if derived classes can be used interchangeably with base classes without altering the correctness of the program.

Exercise 5: The Local Settings Object
Objective: Analyze the implementation of the settings file and evaluate if it adheres to SOLID principles.
Approach:
Find the Settings class and determine what makes it a singleton.
Evaluate if a singleton object is SOLID.
Analyze the storage of hospital types codes and suggest alternative solutions.

HealthShare Referral Manager (HSRM) files can be loaded by:
https://bioinf.nl/~bbarnard/programming4/files/exercise1.zip


## Files:
main.ipynb: Entry point of the application.
parserTypes.py: Defines parser types.
CcsClassification.py
CcsHospitalDataExtracter.py
CcsHospitalInfo.py
FileDownloader.py
LocalSettings.py

Other relevant Python files in the project.

## How to Use:
Clone the Repository.
Open the project in an IDE like VS Code.
Analyze the codebase using the methodology outlined above.


Author:
F. Monfared f.monfared@st.hanze.nl
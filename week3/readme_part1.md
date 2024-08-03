# Generators and Map-Reduce

## Overview
This repository is the part of the project demonstrates the use of generators, list comprehensions, and the application of functions to data collections. The focus is on creating Pythonic and maintainable code.


## Purpose
The purpose of this part is to practice using generators, list comprehensions, and iterables in Python to create more readable, maintainable, and Pythonic code. It also involves refactoring an existing script to improve its structure and apply object-oriented principles.

## Methodology

### Exercise 1: Functions with Data
1. **Creating a Function with Two Parameters:**
   - A function to be applied to the data.
   - The function should return a list of new values created by applying the given function to all elements in the list of data.
2. **Enhancing the Function:**
   - Modify it to accept an arbitrary number of functions.
   - Return a list of lists, each containing the results of applying one of the functions to the data.

### Exercise 2: Refactoring the Web Crawler Code
1. **Encapsulate Code in a Class:**
   - Create a `Crawler` class and Implementing a `crawl_site` method for the main loop.
2. **Refactor Lambda Expressions:**
   - Replacing the lambda expressions with list comprehensions where applicable.
3. **Implement Iterator Pattern:**
   - Introducing an internal pointer for the instance.
   - Refactor the loop in `crawl_site` to use this pointer.
4. **Create Generators:**
   - Implement the `__iter__()` method to create a generator for looping over crawled websites.

## Installation

2. Install dependencies:
import urllib.request
import ssl
from bs4 import BeautifulSoup
import re

The code script that crawls a website with sport clubs in the city Groningen can be downloaded by link provided in assignment.



## Files:
assign3_prog4_part1.ipynb



# How to Use:
Clone the Repository.
Open the project in an IDE like VS Code.
Analyze the codebase using the methodology outlined above.


Author:
F. Monfared f.monfared@st.hanze.nl




# Transpiler-ASD-UniTN

A transpiler that translates pseudocode from Alberto Montresor book and slides in to python.
It can also be used to translate the code from exams solutions.

# Credits:
All the functions inside `known_functions` folder, `GraphDict` class and `Tree` class are translated or taken from Alberto Montresor slides available at
[his site](https://cricca.disi.unitn.it/montresor/). They are available under license [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Usage

- Copy the code from a pdf
- Paste it into a file
- Indent the code (Indentation doesn't get copied)
- Run the script: `python3 main.py [filename]`
- Check the results in the file: `[filename].py` 


    It is advised to reformat the output code with an ide or autopep8

# Flags

- Use `-Y` to skip prompt while converting math operations like floor and ceiling
- Use `--noMath` to make the transpiler ignore the declaration of math.floor and math.ceil
- Use `-o [filename]` to change the output file name, default is [filename].py

# Known Issues

- Still didn't find a consistent way to check for power operator
- Inconsistent recognition of math.floor and math.ceil functions

# TODO

- Move mapping and regex dict to a file so that is easier to edit for the user
- Add more flags
- Add missing data structures

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

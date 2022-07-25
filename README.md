# Transpiler-Montresor

A transpiler that translates pseudocode from Alberto Montresor book and slides in to python.

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

# Known Issues

- Still didn't find a consistent way to check for power operator

# TODO

- Move mapping and regex dict to a file so that is easier to edit for the user
- Add more flags like -o
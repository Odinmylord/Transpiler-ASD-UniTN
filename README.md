# Transpiler-Montresor

A transpiler that translates pseudocode from Alberto Montresor book and slides in to python.

# Usage

- Copy the code from a pdf
- Paste it into a file
- Indent the code (It doesn't get copied)
- Run the script python3 main.py filename


    It is advised to reformat the output code with an ide or autopep8

# Flags

- Use `-Y` to skip prompt while converting math operations like floor and ceiling

# Known Issues

- Still didn't find a consistent way to check for power operator

# TODO

- Move mapping and regex dict to a file so that is easier to edit for the user
- Add more flags like -o
# Transpiler-ASD-UniTN

A transpiler that translates pseudocode from Alberto Montresor book and slides in to python.
It can also be used to translate the code from exams solutions.

# Credits:
All the functions inside `known_functions` folder, and many classes inside `Classes` are translated or taken from Alberto Montresor slides available at
[his site](https://cricca.disi.unitn.it/montresor/). They are available under license [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Usage
## Using pdf as source
- Download a pdf file from [Alberto Montresor site](https://cricca.disi.unitn.it/montresor/teaching/asd/materiale/esercizi/)
- Put it in the same folder of the transpiler
- Run the script: `python3 main.py --pdf [filename].pdf` 

The pdf reader module is made from scratch without installing new libraries so it will probably have problems.<br/>
If you find any feel free to open an issue.

## Copying from pdf
- Copy the code from a pdf
- Paste it into a file
- Indent the code (Indentation doesn't get copied)
- Run the script: `python3 main.py [filename]`
- Check the results in the file: `[filename].py` 


    It is advised to reformat the output code with an ide or autopep8

# Config
Now is possible to easily change the conversion behaviour of the transpiler by editing
the files in the config folder.

# Flags

- `-h`, `--help`            Shows help message and exit
- `-o file.py`            Changes the output file name. Default is [input-file].py
- `--skip-confirmation`, `-Y` Use this flag if you want to skip (accept) all prompts while converting math symbols
- `--no_math`, `-N`         Use this flag if you want the program to ignore all potential math symbols.If --pdf is used it is strongly advised to use this flag
- `--pdf`                 If used the input file should be a .pdf file. The program will read the pdf file and extract all the functions it finds. At the moment it was only tested with past exams
- `--pdf_out file.txt`    The name of the file that the file created by the pdf_reader should have. Default is {input-file}.pdf. (Only works for pdf files)
- `--sub_divisions`       Default to true, if used '=' chars which should be '/' will not be substituted. (Only works for pdf files)
- `--log_files`           Default to false, if used the various states of the conversion are logged in differente files. (Only works for pdf files)
- `--auto_sub_symbols`    Default to true, if used math symbols won't get automatically substituted. A prompt will be shown to the user instead. (Only works for pdf files)
- `--no_math_pdf`         Same as no_math but only for pdf conversion. (Only works for pdf files)
- `--skip_check`          Default to false, if used the program won't wait for user confirmation after reading from the pdf file. (Only works for pdf files)


# Known Issues

- Still didn't find a consistent way to check for power operator (Solved while using `--pdf`)
- Inconsistent recognition of math.floor and math.ceil functions (Solved while using `--pdf`)

# Changelog

- Improved the translation of the "for" instruction
- (pdf) Started using the vertical lines as an indicator for intentation 

# TODO

- Add more flags
- Add missing data structures

# License
Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

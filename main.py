import os
import sys

import Classes
import utils


def main():
    CLASSES = [class_name for class_name in dir(Classes) if not class_name.startswith("__")]
    FUNCTIONS_FILES = [function_file[:-3] for function_file in os.listdir("known_functions") if
                       not function_file.startswith("__")]
    skip_confirmation = False  # Confirmation to convert math.floor or math.ceil
    no_math = False  # If true the script doesn't try to convert floor and ceil known_functions
    files = [arg for arg in sys.argv if not arg.startswith("-")]
    flags = set(sys.argv) - set(files)
    if len(files) != 2 or (len(files) != 3 and "-o" in flags):
        print("Usage: python3 main.py <filename>")
        sys.exit(1)
    filename = files[1]
    out_name = filename + ".py"

    if "-Y" in flags:
        skip_confirmation = True
    elif "--noMath" in flags:
        no_math = True
    elif "-o" in flags:
        flag_index = sys.argv.index("-o")
        out_name = sys.argv[flag_index + 1]

    with open(filename, "r") as f, open(out_name, "w") as out:
        out.write("import math\n")
        out.write("from Classes import " + ", ".join(CLASSES) + "\n")
        for function_file in FUNCTIONS_FILES:
            out.write(f"import known_functions.{function_file}\n")
        out.write("import new_functions.useful_functions\n")
        out.write("from known_functions.trees import BLACK as BLACK\n")
        out.write("from known_functions.trees import RED as RED\n")
        for line in f:
            line = line.rstrip()
            use_regex = False
            if not line:
                continue
            if utils.is_function(line):
                name, params = utils.extract_function(line)
                function_def = utils.build_function(name, params)
                line = function_def
            elif utils.is_declaration(line):
                line = utils.var_declaration(line)
            elif "(" in line:
                line = utils.isolated_function(line)
            else:
                use_regex = True

            line = utils.remap(line, use_regex, skip_confirmation, no_math)
            out.write(line + "\n")


if __name__ == '__main__':
    main()

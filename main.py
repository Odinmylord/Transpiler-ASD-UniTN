import sys

import utils


def main():
    skip_confirmation = False  # Confirmation to convert math.floor or math.ceil
    no_math = False  # If true the script doesn't try to convert floor and ceil functions
    files = [arg for arg in sys.argv if not arg.startswith("-")]
    flags = set(sys.argv) - set(files)
    flags = list(flags)
    if len(files) != 2:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)
    if "-Y" in flags:
        skip_confirmation = True
    elif "--noMath" in flags:
        no_math = True

    filename = files[1]
    with open(filename, "r") as f, open(filename + ".py", "w") as out:
        out.write("import math\n")
        out.write("from Classes import ListOneBased, GraphDict, Tree, Queue, Stack\n")
        out.write("import functions.graphs\n")
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
                var = utils.var_declaration(line)
                line = var
            else:
                use_regex = True
            line = utils.remap(line, use_regex, skip_confirmation, no_math)
            out.write(line + "\n")


if __name__ == '__main__':
    main()

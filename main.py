import sys

import utils


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
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
            line = utils.remap(line, use_regex)
            out.write(line+"\n")


if __name__ == '__main__':
    main()

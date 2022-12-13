import argparse
import os

import pdf_reader
from utility import Classes, conversion_functions

CLASSES = [class_name for class_name in dir(Classes) if not class_name.startswith("__")]
FUNCTIONS_FILES = [function_file[:-3] for function_file in os.listdir("known_functions") if
                   not function_file.startswith("__")]


def main():
    parser = argparse.ArgumentParser(description='List of available flags and correct usage:')
    parser.add_argument("input_file", metavar="file.txt", type=str, nargs=1,
                        help="The input file name, it can also be a .pdf file if --pdf flag is used")
    parser.add_argument("-o", metavar="file.py", type=str, nargs=1,
                        help="The output file name. Default is {input-file}.py")
    parser.add_argument("--skip-confirmation", "-Y", action="store_true",
                        help="Use this flag if you want to skip (accept) all prompts while converting math symbols")
    parser.add_argument("--no_math", "-N", action="store_true",
                        help="Use this flag if you want the program to ignore all potential math symbols."
                             "If --pdf is used it is strongly advised to use this flag")
    parser.add_argument("--pdf", action="store_true",
                        help="If used the input file should be a .pdf file. The program will read the pdf file and "
                             "extract all the functions it finds. At the moment it was only tested with past exams")
    parser.add_argument("--pdf_out", metavar="file.txt", type=str, nargs=1,
                        help="The name of the file that the file created by the pdf_reader should have. "
                             "Default is {input-file}.pdf. (Only works for pdf files)")
    parser.add_argument("--sub_divisions", action="store_false",
                        help="Default to true, if used '=' chars which should be '/' will not be substituted. "
                             "(Only works for pdf files)")
    parser.add_argument("--log_files", action="store_true",
                        help="Default to false, if used the various states of the conversion are logged in "
                             "differente files. (Only works for pdf files)")
    parser.add_argument("--auto_sub_symbols", action="store_false",
                        help="Default to true, if used math symbols won't get automatically substituted. A prompt will "
                             "be shown to the user instead. (Only works for pdf files)")
    parser.add_argument("--no_math_pdf", action="store_true",
                        help="Same as no_math but only for pdf conversion. (Only works for pdf files)")
    parser.add_argument("--skip_check", action="store_true",
                        help="Default to false, if used the program won't wait for user confirmation after reading "
                             "from the pdf file. (Only works for pdf files)")
    args = parser.parse_args()
    filename = args.input_file[0]
    if not args.o:
        args.o = filename + ".py"
    else:
        args.o = args.o[0]
    if args.pdf_out:
        args.pdf_out = args.pdf_out[0]
    if args.pdf:
        filename = pdf_reader.convert_from_pdf(filename, args.pdf_out, args.sub_divisions, args.log_files,
                                               args.auto_sub_symbols, args.no_math_pdf)
    if args.pdf:
        print("File: ", filename, " generated.")
        if not args.skip_check:
            print("Check it before continuing. When done return here and press enter.")
            input()
    with open(filename, "r") as f, open(args.o, "w") as out:
        out.write("import math\n")
        out.write("from utility.Classes import " + ", ".join(CLASSES) + "\n")
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
            if conversion_functions.is_function(line):
                name, params = conversion_functions.extract_function(line)
                function_def = conversion_functions.build_function(name, params)
                line = function_def
            elif conversion_functions.is_declaration(line):
                line = conversion_functions.var_declaration(line, args.no_math, args.skip_confirmation)
            elif "(" in line:
                line = conversion_functions.isolated_function(line)
            else:
                use_regex = True
            line = conversion_functions.remap(line, use_regex, args.skip_confirmation, args.no_math)
            out.write(line + "\n")
    print("File: ", args.o, "generated, you can now run it.")


if __name__ == '__main__':
    main()

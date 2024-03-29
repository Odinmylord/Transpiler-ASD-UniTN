import re
import traceback
from typing import Tuple, List

import known_functions.graphs as graphs
import known_functions.trees as trees
import known_functions.various as various
import utility.utils
from utility import Classes

GRAPHS_FUNCTIONS = [func for func in dir(graphs) if not func.startswith("__")]
TREES_FUNCTIONS = [func for func in dir(trees) if not func.startswith("__")]
VARIOUS_FUNCTIONS = [func for func in dir(various) if not func.startswith("__")]
CLASSES = [new_class for new_class in dir(Classes) if not new_class.startswith("__")]
KNOWN_FUNCTIONS = GRAPHS_FUNCTIONS + TREES_FUNCTIONS + VARIOUS_FUNCTIONS
FUNCTIONS_MAPPER = {
    "graphs": GRAPHS_FUNCTIONS,
    "trees": TREES_FUNCTIONS
}

TYPES_LIST = ["int", "float", "bool", "string", "boolean"]

STRUCTS_LIST = utility.utils.json_loader("struct_list.json")
TAB_SPACES = 4
INDENTATION_TYPE = " "

MAPPING = utility.utils.json_loader("mapping.json")
REGEXES = utility.utils.json_loader("regexes.json")

skip = []
ignore = []


def is_function(line: str) -> bool:
    """
    :param line: a line of pseudo-code
    :return: True if the line is a function, False otherwise
    :return:
    """
    return line[0].isalpha() and not "=" in line and line.count("(") == 1 and line[-1] == ")"


def extract_function(line: str) -> Tuple[str, dict]:
    """
    :param line: a line of pseudo-code
    :return: the function's name and params
    :return:
    """
    param_mapping = {}
    if "," in line:
        params = line.split(",")
        params[0] = params[0].split("(")[1]
        params[-1] = params[-1].split(")")[0]
    else:
        params = [line.split("(")[1].split(")")[0]]
    for param in params:
        tokens = param.strip().split(" ")
        parameter = tokens[-1]
        param_type = "".join(tokens[:-1])
        param_mapping[parameter] = param_type if param_type in TYPES_LIST else "list"
        param_mapping[parameter] = STRUCTS_LIST.get(param_type, param_type)
    name = line[:line.index("(")]
    name = name if " " not in name else name.split(" ")[-1]
    return name, param_mapping


def build_function(name: str, params: dict) -> str:
    """
    :param name: the function name
    :param params: the function params
    :return: the function definition
    """
    function_def = "def " + name + "("
    for param in params:
        param_type = params[param]
        if param_type in TYPES_LIST:
            function_def += param + ": " + param_type
        elif param_type in STRUCTS_LIST.values():
            function_def += param + ": " + param_type
        else:
            function_def += param + ": ListOneBased"
        function_def += ", "
    function_def = function_def[:-2] + "):\n"
    function_def = function_def.replace("-", "_")
    return function_def


def is_declaration(line: str) -> bool:
    """
    :param line: a line of pseudo-code
    :return: True if the line is a variable declaration, False otherwise:
    """
    return_value = False
    line = line.strip()
    if " " not in line:
        return return_value

    tokens = line.split(" ")
    if tokens[0] in TYPES_LIST or tokens[0] in STRUCTS_LIST or (tokens[0][-1] == "[" and tokens[0][:-1] in TYPES_LIST):
        return_value = True
    return return_value


def is_known_function(tokens: List[str]) -> bool:
    if not tokens or "(" not in tokens[-1]:
        return False
    return_value = False
    func_call = tokens[-1] if tokens[-1][0] != "(" else "".join(tokens[-2:])
    parenthesis_index = func_call.index("(")
    function_name = func_call[:parenthesis_index]
    if function_name in KNOWN_FUNCTIONS:
        return_value = True
    return return_value


def get_func_call(tokens: List[str]) -> str:
    return "".join(tokens[-2:]) if tokens[-1][0] == "(" else tokens[-1]


def get_func_declaration(func: str) -> Tuple[str, str]:
    func_name = func[:func.index("(")]
    for module in FUNCTIONS_MAPPER:
        if func_name in FUNCTIONS_MAPPER.get(module, []):
            return func_name, module


def var_declaration(line: str, no_math: bool, skip_confirmation: bool) -> str:
    """
    :param line: a line of pseudo-code
    :param no_math: if true math symbol conversion is ignored
    :param skip_confirmation: default all the conversion prompt to yes
    :return: the variable declaration
    """
    left_offset = left_offset_calculator(line)
    line = line.strip()
    tokens = line.split(" ")
    compacted_tokens = []
    if "(" in line:
        compacted_tokens = compact_tokens(tokens)
    equal_index = line.index("=")
    default_value = ""
    name_part = line[:equal_index].strip()
    var_name = name_part.split(" ")[-1] if " " in name_part else None
    if not no_math:
        line = check_math_func(line, skip_confirmation)
    if line.count("=") == 2 and "iif" not in line:
        try:
            default_value = line[line.index("{") + 1:line.index("}")]
        except ValueError as e:
            print(traceback.format_exc())
            print(line)
            print("The line above gave an error, maybe because you forgot to replace an = with a / or "
                  "another pair of chars")
            import sys
            sys.exit(3)
    if is_known_function(compacted_tokens):
        func_call = get_func_call(compacted_tokens)
        function_name, function_module = get_func_declaration(func_call)
        var = left_offset + var_name + " =" + f" {function_module}." + func_call

    elif "[" in name_part and "new " in line:
        new_pos = tokens.index("new")
        # The two minuses have different unicode values
        if default_value and default_value[0] in ["−", "-"]:
            default_value = default_value[1:] + "*-1"
        struct_declaration = "".join(tokens[new_pos + 1:])  # in the final part of the string there are the sizes
        var_type = array_declaration(struct_declaration, default_value)
        var = left_offset + var_name + " = " + var_type

    else:
        for token in compacted_tokens:
            if token in STRUCTS_LIST:
                line = line.replace(token, STRUCTS_LIST.get(token))
        var = left_offset + line[line.index(" ") + 1:]
    return var


def isolated_function(line: str) -> str:
    left_offset = left_offset_calculator(line)
    line = line.strip()
    tokens = line.split(" ")
    compacted_tokens = []
    if "(" in line:
        compacted_tokens = compact_tokens(tokens)
    if is_known_function(compacted_tokens):
        func_call = get_func_call(compacted_tokens)
        function_name, function_module = get_func_declaration(func_call)
        line = left_offset + f"{function_module}." + func_call.strip()
    else:
        line = left_offset + line
    return line


def array_declaration(struct_declaration: str, default_value: str = None):
    """
    Takes a list of sizes for arrays like [1...n][1...9][n] and returns the array that fits this description.
    The three dots between the lower and upper bound are necessary.
    :param struct_declaration: a string containing the sizes of the different arrays
    :param default_value: the default value to initialize the arrays
    :return: the declaration for the given array
    """
    levels = []
    if default_value:
        struct_declaration = struct_declaration[:struct_declaration.index("=")]
    while "[" in struct_declaration:
        left_par_index = struct_declaration.index("]")
        right_par_index = struct_declaration.index("[")
        initialization_size = struct_declaration[right_par_index + 1:left_par_index]
        initialization_size = initialization_size.replace("...", ", ")
        if "," in initialization_size and initialization_size[0] != "1":
            # In cases like 2...n the first cell exists and is full so that it doesn't give problems
            initialization_size = "1" + initialization_size[1:]
        levels.append(initialization_size)
        struct_declaration = struct_declaration[left_par_index + 1:]
    first_level = levels.pop(0)
    base = f"ListOneBased([\"__\" for _ in range({first_level}+1)])"
    for level in levels:
        array = f"ListOneBased([\"__\" for _ in range({level}+1)])"
        base = base.replace("\"__\"", array)
    if default_value:
        base = base.replace("\"__\"", default_value)
    return base


def inline_if_translator(line: str) -> str:
    while line.count("iif"):
        iif_index = line.rindex("iif")
        count = 0
        index = iif_index + 3
        for c in line[iif_index + 3:]:
            index += 1
            if c == " ":
                continue
            if c == "(":
                count += 1
            elif c == ")":
                count -= 1
            if count == 0:
                break
        iif_to_change = line[iif_index:index]
        tokens = iif_to_change.split(",")
        condition = tokens[0][tokens[0].index("(") + 1:]
        if "=" in condition.split(" "):
            condition = condition.replace("=", "==", 1)
        failure = tokens[-1][:-1]
        success = ",".join(tokens[1:len(tokens) - 1])
        new_iif = "(" + success + " if " + condition + " else " + failure + ")"
        line = line.replace(iif_to_change, new_iif)
    return line


def for_translator(line: str):
    tokens = line.split(" ")
    var_name = tokens[1]
    down_to = "downto" in line
    limiter = "downto" if down_to else "to"
    second_block_index = tokens.index(limiter)
    base = tokens[tokens.index("=") + 1:  second_block_index]
    base = " ".join(base)
    step_index = tokens.index("step") if "step" in line else len(tokens)
    try:
        limit = " ".join(tokens[second_block_index + 1: step_index]).strip(":")
    except IndexError:
        print(traceback.format_exc())
        print(line)
        print("Error while translating the for in the line above, maybe you forgot to put a ∈ symbol")
        import sys
        sys.exit(2)
    step = ""
    if down_to:
        step = ", -1"
    elif step_index != len(tokens):
        step = "," + " ".join(tokens[step_index+1:]).strip(":")
    line = f"for {var_name} in range({base}, {limit}+1{step}):"
    return line


def remap(line: str, regex=False, skip_confirmation: bool = False, no_math: bool = False) -> str:
    """
    :param no_math: If true the script doesn't try to convert floor and ceil known_functions
    :param skip_confirmation: if true all confirmations for conversion of math known_functions are skipped
    :param regex: if true regexes are used to convert, it also means that the line isn't a function declaration
    :param line: a line of pseudo-code
    :return: the line with the variables remapped
    """
    left_offset = left_offset_calculator(line)
    original_line = line
    line = line.strip()
    if not no_math and not line.startswith("def"):
        line = check_math_func(line, skip_confirmation)
    for key in MAPPING:
        line = line.replace(key, MAPPING[key])
    if regex:
        for regex in REGEXES:
            regex = regex.replace("\\\\", "\\")
            line = re.sub(regex, REGEXES[regex], line)

    if "iif" in line:
        line = inline_if_translator(line)
    if line.startswith("for") and "∈" not in original_line and "in" not in line:
        line = for_translator(line)
    elif line.startswith("for"):
        if "- {" in line:
            lists = line[line.index("in") + 2:line.index(":")]
            new_lists = lists.replace("{", "[").replace("}", "]").replace("-", ",")
            new_lists = " new_functions.useful_functions.subtract_lists(" + new_lists + ")"
            line = line.replace(lists, new_lists)
        else:
            line = line.replace("{", "range(").replace("}", "+1)")
    if line.startswith("print "):
        line = line.replace("print ", "print(")
        line = line.replace("...", ":")  # May break something
        if "#" in line:
            line = line.replace("#", ")#")
        else:
            line += ")"
    if "$" in line:
        #swap
        parts = line.split("$")
        line = line.replace("$", ",")
        line += f" = {parts[1]}, {parts[0]}"
    if "|" in line:
        line = abs_value(line)
    if "sort" in line and not line.startswith("def"):
        target = line[line.index("sort"):]
        target = target[:target.index(")")]
        line = line.replace("sort", "list.sort")
        if "," in target:
            new_target = target.split(",")[0]
            line = line.replace(target, new_target)
    return left_offset + line


def check_math_func(line: str, skip_confirmation: bool) -> str:
    """
    :param line: the line containing the known_functions
    :param skip_confirmation: if true doesn't prompt user when converting
    :return: the line with the known_functions replaced
    """
    comment_start = line.find("%")
    comment = ""
    if comment_start >= 0:
        comment = line[comment_start:]
        line = line[:comment_start]
    matches = utility.utils.find_patterns(line)
    ask = not skip_confirmation
    for match in matches:
        ask, substitute, group, group_name = utility.utils.ask_user_confirmation(ask, match, skip, ignore)

        if substitute or skip_confirmation:
            line = utility.utils.replace_match(group, group_name, match)
            original_line = utility.utils.restore_line(match.string)
            line = utility.utils.restore_line(line)
            line = line.replace(original_line, line)
    return line + comment


def check_math_func_old(line: str, skip_confirmation: bool) -> str:
    """
    :param line: the line containing the known_functions
    :param skip_confirmation: if true doesn't prompt user when converting
    :return: the line with the known_functions replaced
    """

    start_indexes = {}
    ending_indexes = {}
    last_length = len(line)
    for i in range(last_length):
        char = line[i]
        if char in ['b', 'd']:
            start_indexes[i] = char
        elif char in ['c', 'e']:
            ending_indexes[i] = char
    offset = 0
    for start, end in zip(start_indexes, ending_indexes):
        start_pos = start + offset
        end_pos = end + offset

        if end_pos < start_pos:
            continue

        substitute = False
        if skip_confirmation:
            substitute = True
        else:
            print_string = "Do you want to substitute this two characters with their respective math function?\n" + \
                           line + "\n" + " " * start_pos + "^" + " " * (
                                   end_pos - start_pos - 1) + "^\n" + "Type Y or y to substitute: "
            res = input(print_string)
            if res.lower() == "y":
                substitute = True
        if substitute:
            line = insert_value_in_string(line, ")", end_pos)
            value = "math.floor("
            if start_indexes[start] == "d":
                value = "math.ceil("
            line = insert_value_in_string(line, value, start_pos)
            offset += len(line) - last_length
            last_length = len(line)

    return line


def abs_value(line: str) -> str:
    last_length = len(line)
    start = True
    values = {}
    for i in range(last_length):
        c = line[i]
        if c != "|":
            continue
        values[i] = start
        start = not start
    offset = 0
    for pos in values:
        value = "abs(" if values[pos] else ")"
        line = insert_value_in_string(line, value, pos + offset)
        offset += len(line) - last_length
        last_length = len(line)
    return line


def left_offset_calculator(line: str) -> str:
    """
    :param line: the line to calculate offset of
    :return: a string that represents the indentation for the line
    """
    indent_tab = line.count("\t")
    indent_spaces = len(line) - len(line.lstrip())
    left_offset = TAB_SPACES * INDENTATION_TYPE * indent_tab + " " * indent_spaces
    return left_offset


def insert_value_in_string(string: str, value: str, index: int):
    return string[:index] + value + string[index + 1:]


def comment_formatter(comment_to_format: str) -> str:
    last_comment_line = comment_to_format.split("\n")[-1]
    return "    % " + last_comment_line[last_comment_line.index("(") + 1:last_comment_line.index(")")]


def compact_tokens(tokens: list) -> list:
    compacted = False
    compacted_tokens = tokens
    if "(" in tokens[-1] and ")" in tokens[-1]:
        compacted = True

    if not compacted:
        original_string = " ".join(tokens)
        open_index = original_string.rindex("(")
        first_half = original_string[:open_index]
        second_half = original_string[open_index:]
        second_half = second_half.replace(" ", "")
        compacted_tokens = (first_half + second_half).split(" ")
    return compacted_tokens

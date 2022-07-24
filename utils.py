import re
from typing import Tuple, List

import functions.graphs as graphs

GRAPHS_FUNCTIONS = [func for func in dir(graphs) if not func.startswith("__")]
KNOWN_FUNCTIONS = GRAPHS_FUNCTIONS
FUNCTIONS_MAPPER = {
    "graphs": GRAPHS_FUNCTIONS
}
TYPES_LIST = ["int", "float", "bool", "string"]
STRUCTS_LIST = {
    "Set": "set",
    "Graph": "GraphDict",
    "Node": "int",
    "Tree": "Tree",
    "Queue": "Queue",
    "Stack": "Stack"
}

TAB_SPACES = 4
INDENTATION_TYPE = " "

MAPPING = {
    " then": ":",
    "else": "else:",
    "6 =": "!=",
    " ≤": "<=",
    " ≥": ">=",
    "mod": "%",
    "·": "*",
    "−": "-",
    "∈": "in",
    "foreach": "for",
    " do": ":",
    "nil": "None",
    "false": "False",
    "true": "True",
    "〈": "(",
    "〉": ")",
    " % ": "#  "  # Sicuramente darà problemi ma serve per i commenti
}
REGEXES = {
    "\)(?=\d+)": ")**",  # This is a try to solve the problem of the power that can't be recognized
}


def is_function(line: str) -> bool:
    """
    :param line: a line of pseudo-code
    :return: True if the line is a functions, False otherwise
    :return:
    """
    return line[0].isalpha() and line.count("(") == 1 and line[-1] == ")"


def extract_function(line: str) -> Tuple[str, dict]:
    """
    :param line: a line of pseudo-code
    :return: the functions name and params
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
    :param name: the functions name
    :param params: the functions params
    :return: the functions definition
    :return:
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
    return function_def


def is_declaration(line: str) -> bool:
    """
    :param line: a line of pseudo-code
    :return: True if the line is a variable declaration, False otherwise
    :return:
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
    if "(" not in tokens[-1]:
        return False
    return_value = False
    func_call = tokens[-1]
    parenthesis_index = func_call.index("(")
    function_name = func_call[:parenthesis_index]
    if function_name in KNOWN_FUNCTIONS:
        return_value = True
    return return_value


def get_func_declaration(func: str) -> Tuple[str, str]:
    func_name = func[:func.index("(")]
    for module in FUNCTIONS_MAPPER:
        if func_name in FUNCTIONS_MAPPER.get(module, []):
            return func_name, module


def var_declaration(line: str) -> str:
    """
    :param line: a line of pseudo-code
    :return: the variable declaration
    :return:
    """
    left_offset = left_offset_calculator(line)
    line = line.strip()
    tokens = line.split(" ")
    equal_index = line.index("=")
    default_value = ""
    name_part = line[:equal_index].strip()
    var_name = name_part.split(" ")[-1] if " " in name_part else None
    if line.count("=") == 2:
        default_value = line[line.index("{") + 1:line.index("}")]
    if is_known_function(tokens):
        function_name, function_module = get_func_declaration(tokens[-1])
        var = left_offset + var_name + " =" + f" functions.{function_module}." + tokens[-1].strip()

    elif "[" in name_part and "new" in line:
        new_pos = tokens.index("new")
        # i due meno sembrano uguali ma non lo sono
        if default_value and default_value[0] in ["−", "-"]:
            default_value = default_value[1:] + "*-1"
        struct_declaration = "".join(tokens[new_pos + 1:])  # prende la parte finale dove si trova la dimensione
        var_type = array_declaration(struct_declaration, default_value)
        var = left_offset + var_name + " = " + var_type

    else:
        var = left_offset + line[line.index(" ") + 1:]
    return var


def array_declaration(struct_declaration: str, default_value: str = None):
    levels = []
    if default_value:
        struct_declaration = struct_declaration[:struct_declaration.index("=")]
        print(struct_declaration)
    while "[" in struct_declaration:
        left_par_index = struct_declaration.index("]")
        right_par_index = struct_declaration.index("[")
        initialization_size = struct_declaration[right_par_index + 1:left_par_index]
        initialization_size = initialization_size.replace("...", ", ")
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
        iif_index = line.index("iif")
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
        failure = tokens[-1][:-1]
        success = ",".join(tokens[1:len(tokens) - 1])
        new_iif = success + " if " + condition + " else " + failure
        line = line.replace(iif_to_change, new_iif)
    return line


def for_translator(line: str):
    tokens = line.split(" ")
    var_name = tokens[1]
    base = tokens[3]
    limit = tokens[5].strip(":")
    return f"for {var_name} in range({base}, {limit}+1):"


def remap(line: str, regex=False, skip_confirmation: bool = False) -> str:
    """
    :param skip_confirmation: if true all confirmations for conversion of math functions are skipped
    :param regex: if true regexes are used to convert
    :param line: a line of pseudo-code
    :return: the line with the variables remapped
    :return:
    """
    left_offset = left_offset_calculator(line)
    original_line = line
    line = line.strip()
    for key in MAPPING:
        line = line.replace(key, MAPPING[key])
    if regex:
        for regex in REGEXES:
            line = re.sub(regex, REGEXES[regex], line)

    if "iif" in line:
        line = inline_if_translator(line)
    if regex:  # Means that this isn't a func or variable declaration
        line = check_math_func(line, skip_confirmation)
    if line.startswith("for") and "∈" not in original_line:
        line = for_translator(line)
    if line.startswith("print"):
        line = line.replace("print", "print(")
        line += ")"
    return left_offset + line


def left_offset_calculator(line: str) -> str:
    indent_tab = line.count("\t")
    indent_spaces = len(line) - len(line.lstrip())
    left_offset = TAB_SPACES * INDENTATION_TYPE * indent_tab + " " * indent_spaces
    return left_offset


def check_math_func(line: str, skip_confirmation: bool) -> str:
    start_indexes = {}
    ending_indexes = {}
    for i in range(len(line)):
        char = line[i]
        if char in ['b', 'd']:
            start_indexes[i] = char
        elif char in ['c', 'e']:
            ending_indexes[i] = char
    if start_indexes and ending_indexes and len(start_indexes) != len(ending_indexes):
        print("Math functions conversion found an inconsistency between starting and ending values")
    original_length = len(line)
    offset = 0
    for start, end in zip(start_indexes, ending_indexes):
        start_pos = start + offset
        end_pos = end + offset
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
            offset += len(line) - original_length
    return line


def insert_value_in_string(string: str, value: str, index: int):
    return string[:index] + value + string[index + 1:]

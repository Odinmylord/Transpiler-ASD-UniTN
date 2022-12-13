import json
import os
import re
import typing


def json_loader(file_name: str) -> dict:
    if not os.path.isdir("config"):
        raise FileNotFoundError("can't find config dir")
    elif not os.path.isfile("./config/" + file_name):
        raise FileNotFoundError(f"Can't find file {file_name}")
    with open("./config/" + file_name, "r") as f:
        return json.load(f)


# This part will be useful only for copied and pasted text I hope

line_sanitizers = json_loader("line_sanitizers.json")
char_pairs = json_loader("char_pairs.json")
char_pairs_with_space = json_loader("char_pairs_with_space.json")
char_pairs_regexes = [re.compile(char_pair[0] + fr"(?P<{char_pair[0]}{char_pair[1]}>[^\s].*?)" + char_pair[1]) for
                      char_pair in char_pairs]
char_pairs_with_space_regexes = [re.compile(char_pair[0] + fr"(?P<{char_pair[0]}{char_pair[1]}>.+?)" + char_pair[1]) for
                                 char_pair in char_pairs_with_space]
total_regex = "|".join([reg.pattern for reg in char_pairs_regexes + char_pairs_with_space_regexes])


def sanitize_line(line: str) -> str:
    """Substitutes parts of the string in order to avoid false positives while checking for symbol patterns"""
    for sanitizer in line_sanitizers:
        new_val = line_sanitizers.get(sanitizer)
        line = line.replace(sanitizer, new_val)
    return line


def restore_line(line: str) -> str:
    """Restores the parts of the string that were substituted by sanitize_line function"""
    for sanitizer in line_sanitizers:
        new_val = line_sanitizers.get(sanitizer)
        line = line.replace(new_val, sanitizer)
    return line


def find_patterns(text: str) -> typing.List[re.match]:
    """Matches the patterns defined in the config folder in the char_pairs*.json files after sanitizing the text"""
    matches = []
    for line in text.split("\n"):
        line = sanitize_line(line)
        matches = matches + [match for match in re.finditer(total_regex, line)]
    return matches


def valid_group(match: re.match) -> typing.Tuple[str, str]:
    group = None
    group_name = None
    for possible_group in match.groupdict():
        possibility = match.groupdict().get(possible_group)
        if possibility:
            group = possibility
            group_name = possible_group
    return group, group_name


def replace_match(group: str, group_name: str, match: re.match) -> str:
    if group_name in char_pairs:
        first_sub_char = char_pairs.get(group_name)[0]
        second_sub_char = char_pairs.get(group_name)[1]
        new_line = re.sub(match.re, first_sub_char + group + second_sub_char, match.string)
    elif group_name in char_pairs_with_space:
        first_sub_char = char_pairs_with_space.get(group_name)[0]
        second_sub_char = char_pairs_with_space.get(group_name)[1]
        new_line = re.sub(match.re, first_sub_char + group + second_sub_char, match.string)
    else:
        print(group_name, group, match)
        raise ValueError("I don't know how we got here")
    return new_line


def ask_user_confirmation(ask, match, skip, ignore):
    res = ""
    substitute = False
    group, group_name = valid_group(match)
    if group_name not in ignore and group not in skip:
        new_vals = char_pairs.get(group_name, None) or char_pairs_with_space.get(group_name, None)

        line = match.string
        if ask:
            print_string = f"Do you want to substitute the first and last char of this string?\n" + \
                           group_name[0] + restore_line(group) + group_name[1] + \
                           "\nit would become:\n" + \
                           new_vals[0] + restore_line(group) + new_vals[1] + \
                           "\nfound in: " + \
                           restore_line(line.strip()) + \
                           "\n(Type y to substitute, stop to interrupt the process, " \
                           "skip to ignore all identical patterns or i to ignore this char pair) "
            res = input(print_string)
        if res.lower() == "y":
            substitute = True
        elif res.lower().strip() == "stop":
            ask = False
        elif res.lower().strip() == "skip":
            skip.append(group)
        elif res.lower().strip() == "i":
            ignore.append(group_name)
    return ask, substitute, group, group_name


def get_symbol_from_char(c: str) -> typing.Union[str, None]:
    return_val = None
    for key in char_pairs:
        index = key.find(c)
        if index >= 0:
            return_val = char_pairs.get(key, [None for _ in range(index)])[index]
    for key in char_pairs_with_space:
        index = key.find(c)
        if index >= 0:
            return_val = char_pairs_with_space.get(key, [None for _ in range(index)])[index]
    return return_val

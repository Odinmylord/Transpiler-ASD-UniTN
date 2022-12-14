import json
import re
import zlib

import utility.utils
from utility.conversion_functions import TYPES_LIST, STRUCTS_LIST, comment_formatter

MAGIC_INDENTATION_SIZE_NUMBER = 17
# TODO find a way to avoid manually mapping symbol conversions
pdf_conversions = utility.utils.json_loader("pdf_conversions.json")


def convert_from_pdf(file: str, out_file_name=None, sub_divisions=True, log_files=False, auto_sub_symbols=True,
                     no_math=False) -> str:
    """
    :param file: file with .pdf from which the code should be extracted
    :param out_file_name: output file name, if None is passed it will become {file}.txt
    :param sub_divisions: if True the program automatically substitutes the "=" that should be "/"
    :param log_files: if True the various states of the conversion are logged in differente files
    :param auto_sub_symbols: if True all the matched math symbols get automatically substituted
    :param no_math: if True all potential math symbols will be ignored.
    :return: a string containing the name of the file with the converted text
    """
    if file[-4:] != ".pdf":
        raise FileNotFoundError("Invalid input file name provided. It should have extension .pdf")
    if not out_file_name:
        out_file_name = file[:-4] + ".txt"
    pdf = open(file, "rb").read()
    stream = rb".*?FlateDecode.*?stream(.*?)endstream"
    streams = re.compile(stream, re.S)
    cont = ""
    for s in streams.findall(pdf):
        s = s.strip(b'\r\n')
        try:
            cont_tmp = zlib.decompress(s)
            cont += str(cont_tmp)
        except:
            pass
    if log_files:
        with open("original_cont.txt", "w") as f:
            f.write(cont)
        with open("original_cont_sep.txt", "w") as f:
            f.write(cont.replace("\\n", "\n"))

    to_replace = re.findall(r"\)[0-9\-]+\(", cont)
    spaces = set()
    joins = set()
    for token in to_replace:
        num = token[1:-1]
        temp_num = num[1:] if num[0] == "-" else num
        temp_num = int(temp_num)
        if temp_num < 200:
            joins.add(num)
        else:
            spaces.add(num)

    for join_token in joins:
        cont = cont.replace(f"){join_token}(", "")
    for space_token in spaces:
        cont = cont.replace(f"){space_token}(", " ")

    if log_files:
        with open("test.txt", "w") as f:
            f.write(cont)

    new_text = ""
    # After this point there are only license files for the fonts and other data that isn't useful
    cont = cont[:cont.index("<http://www.ams.org>")]

    def print_group(x):
        return "/F" + x.group(1)

    cont = re.sub(r"TJ/F([0-9.]+) [0-9.]+ Tf", print_group, cont)
    cont = cont.replace("\\n", "\n")
    for conversion in pdf_conversions:
        cont = cont.replace(conversion, pdf_conversions[conversion])
    comment_finder_regex = r"\[\(%\)\]TJ.*?\]"
    comments = re.findall(comment_finder_regex, cont, re.S)
    cont = re.sub(comment_finder_regex, "[(INSERT_COMMENT_HERE)]", cont, flags=re.S)

    if log_files:
        with open("test3.txt", "w") as f:
            f.write(cont)

    cont3_blocks = cont.split("BT")
    parts_values = {}
    long_line_regex = r"[0-9 ]{8}[0-9.]{6} [0-9.]{6,7} cm"
    drawn_line_regex = r"\[\d*\]\d d [0-2] J [0-9.]+ w [0-9.]+ [0-9.]+ m \d{3}.\d{2} [0-9.]+ l S"
    pos_regex = r"[0-9.-]+ [0-9.-]+ T[dm] \[\("
    # parts_regex = r"T[dm] \[\((.+?)\)\]" old one that didn't save Font value
    parts_regex = r"(/F[0-9]{1,3})*.*?T[dm] \[\((.+?)\)\]"
    total_parts = 0
    drawn_line_count = 0
    last_pos = 0
    first_time = True
    variation = 0
    is_long_line = False
    power = False
    total_indentation = 0
    for cont3_block in cont3_blocks:
        indentation = 0

        for line in cont3_block.split("\n"):
            if drawn_line_count == 3:
                drawn_line_count = 0
                indentation = 0
                variation = 0
                new_text += "\n\n"
                first_time = True
                is_long_line = False
            if not is_long_line:
                is_long_line = re.match(long_line_regex, line)

            elif re.match(drawn_line_regex, line):  # The line is both long and drawn
                drawn_line_count += 1
                new_text += "\n"
                is_long_line = False
            else:
                is_long_line = False

            if drawn_line_count >= 1:
                parts = re.findall(parts_regex, line)
                positions = re.findall(pos_regex, line)
                spaces = [space.split(" ")[0] for space in positions]
                heights = [height.split(" ")[1] for height in positions]
                starting_pos = actual_pos = float(spaces[0]) if len(spaces) else 0
                count_parts = -1
                first_part = True
                for font, part in parts:
                    # Not sure if it will work every time
                    if not no_math and auto_sub_symbols and font == "/F58":
                        new_val = utility.utils.get_symbol_from_char(part[0])
                        if new_val:
                            part = part.replace(part[0], new_val)
                    variation = 0 if variation < 0 else variation
                    if first_time:
                        last_pos = starting_pos
                        first_time = False
                    count_parts += 1
                    total_parts += 1
                    space_to_add = float(spaces[count_parts])
                    height = float(heights[count_parts])
                    old_part_is_comment = parts_values.get(total_parts - 1, {}).get("part") == "INSERT_COMMENT_HERE"
                    if space_to_add < 0 and old_part_is_comment:
                        space_to_add = parts_values.get(total_parts - 1, {}).get("actually_at", 0)
                    elif space_to_add > 0 and old_part_is_comment:
                        last_pos = parts_values.get(total_parts - 2, {}).get("starting_at", 0)
                    if height < 0 and power:
                        new_text += ")"
                        power = False
                    elif height < 0 or height >= 4:
                        new_text += "\n"
                        first_part = True
                    elif 2 < height < 4:
                        new_text += "**("
                        power = True
                    if not first_part:
                        actual_pos += space_to_add
                    elif first_part and space_to_add < 0:
                        first_part = False
                        starting_pos = actual_pos = actual_pos + space_to_add
                    else:
                        first_part = False
                    if part == "INSERT_COMMENT_HERE":
                        first_part = False
                    if new_text[-1] == "\n":
                        modifier = 0
                        if abs(starting_pos - last_pos) > MAGIC_INDENTATION_SIZE_NUMBER:
                            modifier = int((starting_pos - last_pos) / MAGIC_INDENTATION_SIZE_NUMBER)
                        if abs(starting_pos - last_pos) < 5.72:  # Error Margin
                            pass
                        elif starting_pos < last_pos:
                            variation -= 1
                        elif starting_pos > last_pos:
                            variation += 1
                        variation += modifier
                        total_indentation = indentation + variation
                        new_text += "\t" * total_indentation
                    elif "=" in [new_text[-1], new_text[-2]] and parts_values[total_parts - 1].get("font") == "/F22" \
                            and sub_divisions:
                        new_text = new_text[:-2] if new_text[-2] == "=" else new_text[:-1]
                        new_text += "/ "
                    new_text += part
                    if (abs(space_to_add) > 4.5 or part[-1] == ")") and not part[-1] == ".":
                        new_text += " "
                    parts_values[total_parts] = {
                        "part": part,
                        "font": font,
                        "space": space_to_add,
                        "height": height,
                        "starting_at": starting_pos,
                        "actually_at": actual_pos,
                        "last_at": last_pos,
                        "drawn_line_number": drawn_line_count,
                        "total_indentation": total_indentation
                    }
                    last_pos = starting_pos
            last_line = new_text.split("\n")[-1] if "\n" in new_text else None
            if drawn_line_count == 1 and last_line:
                first_part_index = last_line.index(" ")
                last_line = last_line[first_part_index:]
                new_last_line = last_line
                for var_type in TYPES_LIST + list(STRUCTS_LIST.keys()):
                    var_finder = re.compile(var_type + r"\w")
                    found = re.findall(var_finder, last_line)
                    for el in found:
                        new_var_type = el.replace(var_type, var_type + " ")
                        new_last_line = last_line.replace(el, new_var_type)
                new_last_line = new_last_line.replace(" (", "(")
                new_text = new_last_line.join(new_text.rsplit(last_line, 1))

    if log_files:
        with open("parts_positions.json", "w") as f:
            json.dump(parts_values, f, indent=4)

    new_text = re.sub(r"([=\]])(?![ =\s])", r"\1 ", new_text)

    if not no_math and not auto_sub_symbols:
        matches = utility.utils.find_patterns(new_text)
        ask = True
        skip = []
        ignore = []
        for match in matches:
            ask, substitute, group, group_name = utility.utils.ask_user_confirmation(ask, match, skip, ignore)

            if substitute:
                new_line = utility.utils.replace_match(group, group_name, match)
                original_line = utility.utils.restore_line(match.string)
                new_line = utility.utils.restore_line(new_line)
                new_text = new_text.replace(original_line, new_line)

    for comment in comments:
        new_text = new_text.replace("INSERT_COMMENT_HERE", comment_formatter(comment), 1)

    with open(out_file_name, "w") as f:
        f.write(new_text)
    return out_file_name

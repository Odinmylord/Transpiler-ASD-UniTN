long_line_regex = r"[0-9 ]{8}([0-9.]{6}) [0-9.]{5,7} cm"
drawn_line_regex = r"\[\d*\]\d d [0-2] J [0-9.]+ w [0-9.]+ [0-9.]+ m \d{3}.\d{2,3} [0-9.]+ l S"
# the horizontal line is like 4.98 0 l
horizontal_line_regex = r"\[\d*\]\d d [0-2] J [0-9.]+ w [0-9.]+ [0-9.]+ m (\d{1}.\d+) 0 l S"
# the vertical line is like 0 52.32 l
vertical_line_regex = r"\[\d*\]\d d [0-2] J [0-9.]+ w [0-9.]+ [0-9.]+ m 0 \d+.\d+ l S"

pos_regex = r"[0-9.-]+ [0-9.-]+ T[dm] \[\("
# parts_regex = r"T[dm] \[\((.+?)\)\]" old one that didn't save Font value
parts_regex = r"(/F[0-9]{1,3})*.*?T[dm] \[\((.+?)\)\]"

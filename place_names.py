"""
for creating latex names places for wedding
- names on 4*2 grid
- created by store latex doc strings in a list, then combining
"""

import os
import re
import sys

# ---
# latex doc-strings
# ---

premable = """
\\documentclass{article}
\\usepackage{tabularx}
\\usepackage{tabu} % for horizonal colour
\\usepackage{graphicx}
\\usepackage{adjustbox}
\\usepackage{xcolor} % colou package
\\usepackage{calligra}

% reduce board margins
\\usepackage[margin=0pt,bottom=0pt,top=0pt]{geometry}
% remove page number
\\pagenumbering{gobble}

% user defined table spacing (?)
\\usepackage{array}
\\newcolumntype{P}[1]{>{\\centering\\arraybackslash}p{#1}}
\\newcolumntype{M}[1]{>{\\centering\\arraybackslash}m{#1}}
\\newcolumntype{C}[1]{%
>{\\vbox to 13.5ex\\bgroup\\vfill\\centering\\arraybackslash}%
p{#1}%
<{\\vskip-\\baselineskip\\vfill\\egroup}}  

\\begin{document}

\\centering
\\calligra

    """

# start table
# NOTE: hardcoded dimensions!
table_start = """

\\begin{adjustbox}{width=\\pagewidth}
\\begin{tabular}{C{2.5cm}C{2.5cm} |}

"""

table_end = """

﻿\\end{tabular}
\\end{adjustbox}
\\newpage

"""

# reference table
# - to help keep even when cutting?
reference_table = """
﻿
\\begin{adjustbox}{width=\pagewidth}
\\begin{tabular}{C{2.5cm} | C{2.5cm} }
\\hline
Reference  & Sheet \\\\ 
\\hline
Reference  & Sheet \\\\ 
\\hline
Reference  & Sheet \\\\ 
\\hline
Reference  & Sheet \\\\ 
\\end{tabular}
\\end{adjustbox}

"""

if __name__ == "__main__":

    # output results to current directory
    dir_loc = os.path.dirname(__file__)

    # take file in as argument
    try:
        input_file = sys.argv[1]
        assert bool(re.search('.csv$', input_file), re.IGNORECASE), 'expecting input file to be .csv '
        if os.path.exists(input_file):
            file_path = input_file
        else:
            file_path = os.path.join(dir_loc, input_file)
    except IndexError:
        input_file = "place_names_example_input.txt"
        print(f'input place names file not provide, will use example:\n{input_file}')
        file_path = os.path.join(dir_loc, "place_names_example_input.txt")

    # initial structure of doc
    doc_string = [premable, reference_table, table_start]

    with open(file_path, 'r+') as f:
        names = [line.strip() for line in f.readlines()]

    # HARDCODED:
    max_col = 2
    max_count = 8

    count = 0
    col_count = 0
    for name in names:
        if name == '':
            continue

        # column count
        if col_count < (max_col - 1):
            doc_string += ["\t\t%s &  " % name]
        else:
            doc_string += ["%s \\\\ \n" % name]

        col_count += 1
        if col_count == max_col:
            col_count = 0
        count += 1

        if count == max_count:
            count = 0
            doc_string += [table_end, table_start]

    # in case didn't finish a row
    if col_count != 0:
        doc_string += [" \\\\ \n"]
    # or didn't finish a table
    if count != 0:
        doc_string += [table_end]
    # otherwise drop the newly started table
    else:
        # drop the last table start
        doc_string = doc_string[:-1]

    # doc_string += [reference_table]

    doc_string += ['﻿\\end{document}']

    # write this to a document?
    output = ''.join(doc_string)
    out_file = os.path.join(dir_loc, 'place_names_output.tex')
    print('there following text file will be written to:\n{out_file}')
    print('-'*280)
    print(output)

    with open(out_file, "w") as f:
        f.write(output)

    # TODO: write this directly to file

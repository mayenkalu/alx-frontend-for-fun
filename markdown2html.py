#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html', file=sys.stderr)
        exit(1)

    # Get the input and output file names from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print('Missing {}'.format(input_file), file=sys.stderr)
        exit(1)

    # Process the input Markdown file and convert it to HTML
    with open(input_file) as read:
        with open(output_file, 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            # bold syntax
            for line in read:
                # Replace double asterisks (**) with <b> and </b> for bold text
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)

                # Replace double underscores (__) with <em> and </em> for emphasized text
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # Find and replace the MD5 hashes (within [[...]]) with their corresponding MD5 values
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                # Find and replace occurrences of "((" and "))" with the letter 'C' removed
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_more = re.findall(r'\(\((.+?)\)\)', line)
                if remove_letter_c:
                    remove_c_more = ''.join(
                        c for c in remove_c_more[0] if c not in 'Cc')
                    line = line.replace(remove_letter_c[0], remove_c_more)

                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)

                # Process headings (h1 to h6)
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(
                        heading_num) + headings.strip() + '</h{}>\n'.format(heading_num)

                # Process unordered lists (ul)
                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'

                # Close unordered list if no more list items
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')
                    unordered_start = False

                # Process ordered lists (ol)
                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'

                # Close ordered list if no more list items
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')
                    ordered_start = False

                # Process paragraphs (p) and line breaks (br)
                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                # Write the line to the output file
                if length > 1:
                    html.write(line)

            # Close any open tags before exiting
            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')

    # Exit with a success status code
    exit(0)

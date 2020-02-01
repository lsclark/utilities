
"""
Launches searches in a browser based on entries in an XLS(X) file

Assumes a contiguous rectangular range in the file. Joins entries
within a row with ', ', issues a query for each row in the file.
"""

import argparse
import urllib
from pathlib import Path
from openpyxl import load_workbook
import subprocess


def main(args):
    wb = load_workbook(args.xlsx)
    ws = wb.worksheets[args.sheet]
    range = args.range.split(':')
    data = [', '.join(cell.value for cell in row)
            for row in ws[range[0]:range[1]]]

    searches = []
    for search in data:
        search = urllib.parse.quote(search)
        url = args.url.format(search.replace(" ", "+"))
        searches.append(url)

    subprocess.run([args.browser]+searches)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Launch searches in a browser from an XLSX file")
    parser.add_argument("xlsx", help="Path of XLSX file",
                        type=Path)
    parser.add_argument("range",
                        help="Range to parse (in format `start:end` (eg. D5:G9))")
    parser.add_argument("--browser", default="firefox",
                        help="Browser to use (default: firefox)")
    parser.add_argument("--sheet", type=int, default=0,
                        help="Sheet number (default: 0)")
    parser.add_argument("--url",
                        default="https://www.google.com/search?q={}",
                        help="The search pattern as a single-field format-string")

    args = parser.parse_args()
    main(args)

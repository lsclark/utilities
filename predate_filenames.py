#! /usr/bin/env python3

import re
import datetime
import argparse
from pathlib import Path

RE_END_SCORE = re.compile(r'[-_\s]$')
RE_START_SCORE = re.compile(r'^[-_\s]')


def _make_regex_extract():
    """
    Creates pairs of regexes and date reformatters

    Returns:
        A tuple of 2-tuples:
            1. A compiled regex
            2. A function which takes a 3-tuple and returns a 3-tuple
    """
    def _yyyymmdd(y, m, d):
        return y, m, d

    def _ddmmyyyy(d, m, y):
        return y, m, d
    return ((re.compile(r'(\d{4})[-_\s](\d{1,2})[-_\s](\d{1,2})'),
             _yyyymmdd),
            (re.compile(r'(\d{1,2})[-_\s](\d{1,2})[-_\s](\d{4})'),
             _ddmmyyyy))


RE_DATES = _make_regex_extract()


def find_date_remove(text):
    """
    Find dates in a string and move it to the front

    Args:
        text: A filename string
    Returns:
        A string, or None if unsuccessful
    """
    # Search for each pattern in RE_DATES
    for regex, resolve in RE_DATES:
        match = regex.search(text)
        if match:
            # Extract the match and text before and after
            y, m, d = resolve(*match.groups())
            found = match.group(0)
            pre, post = text.split(found)
            # Remove underscores and whitespace at the end of the prefix
            # and at the start of the suffix
            # eg. asdf_<match>_jkl -> asdf + ... + jkl
            while RE_END_SCORE.search(pre):
                pre = pre[:-1]
            while RE_START_SCORE.search(post):
                post = post[1:]
            if not pre:
                return f'{y}_{int(m):02d}_{int(d):02d}_{post}'
            if not post:
                return f'{y}_{int(m):02d}_{int(d):02d}_{pre}'
            return f'{y}_{int(m):02d}_{int(d):02d}_{pre}_{post}'
    return None


def mtime_fname(path):
    """
    Format a files modification time into YYYY_MM_DD_*

    Args:
        path: A Path to a file
    Returns:
        A Path with a reformatted representation
    """
    mtime = path.stat().st_mtime
    d = datetime.date.fromtimestamp(mtime)
    return path.parent.joinpath(f'{d.year}_{d.month:02d}_{d.day:02d}_{path.name.replace(" ", "_")}')


def _move_date(file):
    """
    Find dates and move them to front

    Uses the date in the filename if possible, otherwise
    uses the modification time

    Args:
        file: A Path
    Returns:
        A Path
    """
    new = find_date_remove(file.stem)
    if new:
        new = new.replace(' ', '_')
        return file.parent.joinpath(new+file.suffix)
    else:
        return mtime_fname(file)


def main(path, commit, preview):
    files = path.glob('*')
    for file in files:
        if file.is_file():
            newname = _move_date(file)
            if file.name != newname.name:
                if preview:
                    print(f'Preview: {file} -> {newname}')
                elif commit:
                    print(f'Renaming: {file} -> {newname}')
                    try:
                        file.rename(newname)
                    except FileExistsError:
                        print(f'--> [Error] {newname} already exists. Skipping')
                else:
                    choice = input(
                        f'Rename - {file} -> {newname} - Continue? Y/[n]: ')
                    if choice and 'y' in choice[0].lower():
                        try:
                            file.rename(newname)
                            print('--> File renamed')
                        except FileExistsError:
                            print(f'--> [Error] {newname} already exists. Skipping')
                    else:
                        print('--> Skipped')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Prefix files with YYYY_MM_DD removing from filename if present')
    parser.add_argument('path',
                        help='Path to directory to be updated',
                        type=Path)
    parser.add_argument('--commit', '-c',
                        help='Commit all edits',
                        default=False, action='store_true')
    parser.add_argument('--preview', '-p',
                        help='Preview without any edits',
                        default=False, action='store_true')
    args = parser.parse_args()
    main(args.path, args.commit, args.preview)

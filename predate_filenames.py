#! /usr/bin/env python3

import re
import os
import datetime
import argparse
from pathlib import Path

RE_END_SCORE = re.compile(r'[-_\s]$')
RE_START_SCORE = re.compile(r'^[-_\s]')

def _make_regex_extract():

    def _yyyymmdd(y,m,d):
        return y,m,d

    def _ddmmyyyy(d,m,y):
        return y,m,d

    return ((re.compile(r'(\d{4})[-_\s](\d{1,2})[-_\s](\d{1,2})'),
            _yyyymmdd),
            (re.compile(r'(\d{1,2})[-_\s](\d{1,2})[-_\s](\d{4})'),
            _ddmmyyyy))

RE_DATES = _make_regex_extract()

def find_date_remove(text):
    for regex, resolve in RE_DATES:
        match = regex.search(text)
        if match:
            y, m, d = resolve(*match.groups())
            found = match.group(0)
            pre, post = text.split(found)
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
    mtime = os.path.getmtime(path)
    d = datetime.date.fromtimestamp(mtime)
    return path.parent.joinpath(f'{d.year}_{d.month:02d}_{d.day:02d}_{path.name}')

def _move_date(file):
    """
    Find dates and move them to front
    """
    new = find_date_remove(file.stem)
    if new:
        return file.parent.joinpath(new+file.suffix)
    else:
        return mtime_fname(file)

def main(path, commit, preview):
    path = Path(path)
    files = path.glob('*.*')
    for file in files:
        newname = _move_date(file)
        if file != newname:
            if preview:
                print(f'Preview: {file} -> {newname}')
            elif commit:
                print(f'Renaming: {file} -> {newname}')
                os.rename(file, newname)
            else:
                choice = input(f'Rename - {file} -> {newname} - Continue? Y/[n]: ')
                if 'y' in choice[0].lower():
                    os.rename(file, newname)
                    print('--> File renamed')
                else:
                    print('--> Skipped')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prefix files with YYYY_MM_DD removing from filename if present')
    parser.add_argument('path',
                        help='Path to directory to be updated')
    parser.add_argument('--commit','-c',
                        help='Commit all edits',
                        default=False, action='store_true')
    parser.add_argument('--preview','-p',
                        help='Preview without any edits',
                        default=False, action='store_true')
    args = parser.parse_args()
    main(args.path, args.commit, args.preview)
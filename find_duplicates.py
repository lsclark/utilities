#! /usr/bin/env python3

import glob
from pathlib import Path
import sys
import hashlib
import argparse
from collections import defaultdict


def md5(fname):
    """
    Generate an md5 hash for a file

    Args:
        fname: A string or Path instance
    Returns:
        The md5 hash as a string
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def select_delete(files):
    """
    Delete one of the files based on interactive user selection

    Args:
        files: A list of Paths
    """
    print('----')
    op = ['[{}] {}'.format(i+1, f) for i, f in enumerate(files)]
    print('[0] DO NOTHING')
    print('\n'.join(op))
    idx = input('SELECT A FILE TO DELETE: ')
    if idx == 0 or not idx:
        print('DOING NOTHING')
        return
    elif 1 <= int(idx) <= len(files):
        delfn = files[int(idx)-1]
        delfn.unlink()
        print('DELETING: {}'.format(delfn))


def main(path, dodel):
    """
    Find duplicated files and potentially delete them

    Duplicate files must have both the same base name and size

    Args:
        path: A Path to a directory
        dodel: Provide deletion dialogue, otherwise just output to console
    """
    # Make dict of files grouped by filesize/basename
    sizes = defaultdict(list)
    for fn in path.rglob('*'):
        if fn.is_file():
            sizes[(fn.stat().st_size, fn.name)].append(fn)

    for files in sizes.values():
            # Group files (same basename/size) by md5 hash
        md5sums = defaultdict(list)
        for fn in files:
            md5sums[md5(fn)].append(fn)
        # Print/delete from groups
        for fns in md5sums.values():
            if len(fns) > 1:
                if dodel:
                    select_delete(fns)
                else:
                    print('  '.join(fns))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Find duplicated files within a directory")
    parser.add_argument("path", type=Path)
    parser.add_argument('--delete', '-d',
                        help="Perform the deletion dialogue (default: just print)",
                        default=False, action='store_true')
    args = parser.parse_args()

    main(args.path, args.delete)

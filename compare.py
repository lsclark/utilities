#! /usr/bin/env python3

from pathlib import Path
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


def main(check, target, invert=False):
    """
    Identify unique files in the checked directory relative to a target

    Unmatched files are printed to stdout

    Args:
        check: The directory to check (a Path)
        target: The reference directory (a Path)
        invert: Print when do match (default: False)
    """
    # Build list of files in reference
    t_sizes = defaultdict(lambda i: defaultdict(list))
    for tf in target.rglob('*'):
        if tf.is_file():
            t_sizes[tf.stat().st_size][tf.name].append(tf)

    # Check files in target for a match in the reference
    for cf in check.rglob('*'):
        if cf.is_file():
            size = cf.stat().st_size
            if size in t_sizes and cf.name in t_sizes[size]:
                for tf in t_sizes[size][cf.name]:
                    if not cf.samefile[tf] and md5(cf) == md5(tf):
                        if invert:
                            print(f'Match: {cf} - {t_sizes[size][cf.name]}')
                        break
                else:
                    if not invert:
                        print(f'No match: {cf})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Check two folders are equivalent")
    parser.add_argument("checkdir",
                        help="The directory to be checked",
                        type=Path)
    parser.add_argument("target",
                        help="The reference directory",
                        type=Path)
    parser.add_argument('--inverse', '-i',
                        help="Show files which match (default: show missing)",
                        default=False, action='store_true', )
    args = parser.parse_args()

    main(args.checkdir, args.target, args.inverse)

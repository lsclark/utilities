#! /usr/bin/env python3

import glob
import os
import sys
import hashlib
import argparse
from collections import defaultdict

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def select_delete(files):
    print('----')
    op = ['[{}] {}'.format(i+1, f) for i,f in enumerate(files)]
    print('[0] DO NOTHING')
    print('\n'.join(op))
    idx = input('SELECT A FILE TO DELETE: ')
    if idx == 0 or not idx:
        print('DOING NOTHING')
        return
    elif 1 <= int(idx) <= len(files):
        delfn = files[int(idx)-1]
        os.remove(delfn)
        print('DELETING: {}'.format(delfn))
    
def main(path, dodel):
    files = glob.glob(os.path.join(path, '**','*.*'), recursive=True)
    
    sizes = defaultdict(dict)
    for fn in files:
        if os.path.isfile(fn):
            sizes[os.path.getsize(fn)][os.path.basename(fn)] = fn

    for size, bases in sizes.items():
        if len(bases)>1:
            md5sums = defaultdict(list)
            for fn in bases.values():
                md5sums[md5(fn)].append(fn)
            for fns in md5sums.values():
                if len(fns)>1:
                    if dodel:
                        select_delete(fns)
                    else:
                        print('  '.join(fns))
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument('--delete','-d',default=False, action='store_true')
    args = parser.parse_args()
    
    main(args.path, args.delete)
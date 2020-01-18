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
    
def main(check, target, invert):
    checkfiles = glob.glob(os.path.join(check, '**','*.*'), recursive=True)
    targetfiles = glob.glob(os.path.join(target, '**','*.*'), recursive=True)
    
    t_sizes = defaultdict(dict)
    for tf in targetfiles:
        t_sizes[os.path.getsize(tf)][os.path.basename(tf)] = tf
    
    for cf in checkfiles:
        size = os.path.getsize(cf)
        base = os.path.basename(cf)
        if size in t_sizes and base in t_sizes[size] and cf != t_sizes[size][base]:
            if invert:
                print('Match: {} - {}'.format(cf, t_sizes[size][base]))
        elif not invert:
            print('No match: {}'.format(cf))
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("checkdir")
    parser.add_argument("target")
    parser.add_argument('--inverse','-i',default=False, action='store_true')
    args = parser.parse_args()
    
    main(args.checkdir, args.target, args.inverse)
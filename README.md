# Utilities
Various python scripts for managing files and other content

## Notes
- Assumes Python 3.6+
- All scripts use argparse

## Contents

### compare.py
Check two folders are equivalent by finding, for each file in a directory, a matching file in a reference.

### find_duplicates.py
Find duplicated files within a single directory

### predate_filenames.py
Identify dates in filenames and move them to the front as YYYY_MM_DD. Falls back to using the modification time. 
#!/usr/bin/env python

import sys

def convert_line(maf_line):
    columns = maf_line.split('\t')
    chromosome = 'chr' + columns[4]
    start = str(int(columns[5]) - 1)
    end = columns[6]
    return '\t'.join([chromosome, start, end])

def convert_maf(maf_path, bed_path):
    with open(maf_path) as maf:
        maf_header = next(maf)
        # bed_header = "track name=ohsu type=bedDetail db=hg38"
        # bed_rows = [bed_header]
        bed_rows = []
        for line in maf:
            bed = convert_line(line)
            bed_rows.append(bed)

    with open(bed_path, 'w') as bed:
        for bed_row in bed_rows:
            bed.write(bed_row + "\n")

if __name__ == '__main__':
    maf_path = sys.argv[1]
    bed_path = sys.argv[2]

    convert_maf(maf_path, bed_path)

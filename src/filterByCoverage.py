import sys
import sam_fields
import readsam
import numpy as np

def calculateCoverage(file_name):
    coverage = {}
    f = readsam.readSamRecords(file_name)
    for samList in f:
        pos = int(samList[sam_fields.POSITION])
        max_len = pos + len(samList[sam_fields.SEQ])
        if pos > 0:
            for i in range(pos, max_len):
                if i not in coverage:
                    coverage[i] = 0
                coverage[i] += 1
    return coverage

def readInPositions(s, e, positions):
    for p in positions:
        if p >= s and p < e:
            return True
    return False

def filterByPositions(in_file, out_file, positions):
    f = readsam.readSamRecords(in_file)
    with open(out_file, 'w') as out:
        for samList in f:
            pos = int(samList[sam_fields.POSITION])
            max_len = pos + len(samList[sam_fields.SEQ])
            if pos > 0 and not readInPositions(pos, max_len, positions):
                out.write('\t'.join(samList) + '\n')

def main():
    file_name = sys.argv[1]
    sigmas = int(sys.argv[2])
    if len(sys.argv) > 3:
        out_file_name = sys.argv[3]
    else:
        out_file_name = file_name[0:-4] + "_coverage_cleanded.sam"

    coverage = calculateCoverage(file_name)
    mean = np.mean(coverage.values())
    std = np.std(coverage.values())
    threshold1 = mean - sigmas * std
    threshold2 = mean + sigmas * std
    filterByPositions(file_name, out_file_name, [k for k, v in coverage.items() if v > threshold1 and v < threshold2])


if __name__ == "__main__":
    sys.exit(main())
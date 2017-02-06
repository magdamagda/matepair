import sys
import src.sam_fields
import src.readsam
import math

def calculateMeanSigma(file_name):
    s= 0
    s2 = 0
    count = 0
    f = src.readsam.readSamRecords(file_name)
    insert_sizes = []
    for samList in f:
        l = abs(int(samList[src.sam_fields.LEN]))
        s += l
        s2 += l*l
        count += 1
        insert_sizes.append(l)
    mean = s/count
    sigma = math.sqrt(s2/count - mean*mean)
    return mean, sigma


def main():
    file_name = sys.argv[1]
    print calculateMeanSigma(file_name)


if __name__ == "__main__":
    sys.exit(main())
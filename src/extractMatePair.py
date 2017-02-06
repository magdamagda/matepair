import sys
import src.sam_fields
import src.readsam
import math

def isMatepair(l, threshold):
    if l > threshold:
        return True
    return False

def extractmp(file_name, mp_file, pe_file, threshold):
    sum_mp = 0
    sum_pe = 0
    sum_mp2 = 0
    sum_pe2 = 0
    count_mp = 0
    count_pe = 0
    f = src.readsam.readSamRecords(file_name)
    with open(mp_file, 'w') as mpf, open(pe_file, 'w') as pef:
        for samList in f:
            l = abs(int(samList[src.sam_fields.LEN]))
            if isMatepair(l, threshold):
                sum_mp += l
                sum_mp2 += l*l
                count_mp += 1
                mpf.write('\t'.join(samList) + '\n')
            else:
                sum_pe += l
                sum_pe2 += l*l
                count_pe += 1
                pef.write('\t'.join(samList) + '\n')
    mean_mp = sum_mp/count_mp
    mean_pe = sum_pe/count_pe
    sigma_mp = math.sqrt(sum_mp2/count_mp - mean_mp*mean_mp)
    sigma_pe = math.sqrt(sum_pe2/count_pe - mean_pe*mean_pe)
    return mean_mp, sigma_mp, mean_pe, sigma_pe


def main():
    file_name = sys.argv[1]
    threshold = float(sys.argv[2])
    mp_file_Name = file_name[0:-4] + "_mp.sam"
    pe_file_name = file_name[0:-4] + "_pe.sam"
    print extractmp(file_name, mp_file_Name, pe_file_name, threshold)


if __name__ == "__main__":
    sys.exit(main())
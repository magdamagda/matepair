import sys
import readsam
import SV
import matplotlib.pyplot as plt
import numpy as np
import filterReads
import const

def calculateHistogram(reads):
    insert_sizes = [abs(r.templateLength) for r in reads]
    insert_sizes = filter(lambda x: x != 0, insert_sizes)
    hist = np.histogram(insert_sizes, 10)
    #plt.figure(2)
    plt.bar(hist[1][0:-1], hist[0])
    plt.show()
    return hist

def main():
    file_name = sys.argv[1]
    #file_name = "../testFiles/neuroblastoma.sam"
    read_type = const.MIX

    # read reads from sam file
    samFile = readsam.readSamFile(file_name)

    # filter: delete noise, remove reads in densly covered areas
    samFile = filterReads.filterReadsByCoverage(samFile)

    # extract split and discordant reads
    samFile = filterReads.extractSplitReads(samFile)

    pe_short, pe_long, abnormal_orient_pe, mp_short, mp_long, abnormal_orient_mp = [], [], [], [], [], []
    if read_type == const.MIX:
        mate_pair, pair_end = filterReads.extractMatePairReadsByOtsuthreshold(samFile.discordant)
        mp_short, mp_long  = filterReads.findAbnormalInsertSizeReads(mate_pair)
        pe_short, pe_long = filterReads.findAbnormalInsertSizeReads(pair_end)
        abnormal_orient_mp = filterReads.findAbnormalOrientationReads(samFile.discordant, "RF")
        abnormal_orient_pe = filterReads.findAbnormalOrientationReads(samFile.discordant, "FR")
    elif read_type == const.MATE_PAIR:
        abnormal_orient_mp = filterReads.findAbnormalOrientationReads(samFile.discordant, "RF")
        mp_short, mp_long = filterReads.findAbnormalInsertSizeReads(samFile.discordant)
    elif read_type == const.PAIR_END:
        abnormal_orient_pe = filterReads.findAbnormalOrientationReads(samFile.discordant, "FR")
        mp_short, mp_long = filterReads.findAbnormalInsertSizeReads(samFile.discordant)


    # some smart algorithm for grouping and namig SV
    # breakPoints = SV.detectSV(samFile.split, pe_short, pe_long, abnormal_orient_pe, mp_short, mp_long, abnormal_orient_mp)


if __name__ == "__main__":
    sys.exit(main())
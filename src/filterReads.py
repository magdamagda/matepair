from coverage import calculateCoverage
import numpy as np
import const
import otsu

def filterReadsByCoverage(samFile):

    cov = calculateCoverage(samFile.reads)
    # print cov
    #median = np.median(cov.values())
    mean = np.mean(cov.values())
    #max_cov = max(cov.values())
    #min_cov = min(cov.values())
    std = np.std(cov.values())
    threshold = mean + 3 * std
    for i in cov:
        if cov[i] > threshold:
            samFile.deleteReadInPos(i)

    #cov = calculateCoverage(samFile.reads)

    return samFile

def extractSplitReads(samFile):
    for i in range(0, len(samFile.reads)):
        if 'SA:' in samFile.reads[i].tags:
            samFile.markAsSplitRead(i)
        else:
            samFile.markAsDiscordantRead(i)

    return samFile

def extractMatePairReadsByOrienatation(reads):
    mate_pair = []
    pair_end = []
    abnormal_orientation = []
    unmapped = []
    for r in reads:
        if r.flag & 0x04 or r.flag & 0x08:
            unmapped.append(r)
        else:
            orientation1 = 'R' if r.flag & 0x10 else 'F'
            orientation2 = 'R' if r.flag & 0x20 else 'F'
            orientation = orientation1 + orientation2
            if orientation in ['RR', 'FF']:
                abnormal_orientation.append(r)
            elif (orientation == 'RF' and r.pos < r.nextPos) or (orientation == 'FR' and r.pos > r.nextPos):
                mate_pair.append(r)
            elif (orientation == 'FR' and r.pos < r.nextPos) or (orientation == 'RF' and r.pos > r.nextPos):
                pair_end.append(r)

    return mate_pair, pair_end, abnormal_orientation, unmapped

def findAbnormalOrientationReads(reads, orientation):
    abnormals = []
    orientation_reversed = orientation[::-1]
    for r in reads:
        if not (r.flag & 0x04 or r.flag & 0x08):
            orientation1 = 'R' if r.flag & 0x10 else 'F'
            orientation2 = 'R' if r.flag & 0x20 else 'F'
            o = orientation1 + orientation2
            if not((o == orientation and r.pos < r.nextPos) or (o == orientation_reversed and r.pos > r.nextPos)):
                abnormals.append(r)
    return abnormals

def findAbnormalInsertSizeReads(reads):
    short = []
    long = []
    insert_sizes = [abs(r.templateLength) for r in reads]
    insert_sizes = filter(lambda x: x != 0, insert_sizes)
    mean = np.mean(insert_sizes)
    std = np.std(insert_sizes)
    t1 = mean - std
    t2 = mean + std
    for r in reads:
        if r.templateLength > t2:
            long.append(r)
        elif r.templateLength < t1:
            short.append(r)
    return short, long

def extractMatePairReadsByOtsuthreshold(reads):
    mate_pair = []
    pair_end = []
    insert_sizes = [abs(r.templateLength) for r in reads]
    insert_sizes = filter(lambda x: x != 0, insert_sizes)
    threshold = otsu.otsu_threshold(insert_sizes, 100)
    for r in reads:
        if r.templateLength<=threshold:
            pair_end.append(r)
        else:
            mate_pair.append(r)
    mean = np.mean([abs(r.templateLength) for r in pair_end])
    mean = np.mean([abs(r.templateLength) for r in mate_pair])
    return mate_pair, pair_end
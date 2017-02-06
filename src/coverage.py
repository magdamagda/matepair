def calculateCoverage(reads):
    coverage = {}
    for read in reads:
        max_len = read.pos + len(read.seq)
        #if len(coverage) < max_len:
            #coverage += [0] * (max_len - len(coverage))
        for i in range(read.pos-1, max_len-1):
            if i not in coverage:
                coverage[i] = 0
            coverage[i] += 1

    return coverage
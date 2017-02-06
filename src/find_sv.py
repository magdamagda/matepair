import sys
import sam_fields
import readsam
import SV
import sam

def findAbnormalReads(file_name, mean, sigma, orientation):
    short = []
    long = []
    bad_orienatation = []
    interchromosomal = []
    unmapped = []
    orientation_reversed = orientation[::-1]
    f = readsam.readSamRecords(file_name)
    for samList in f:
        read = sam.Read(samList)
        if read.templateLength > mean + sigma:
            long.append(read)
        elif read.templateLength<mean-sigma:
            short.append(read)
        if read.flag & 0x04 or read.flag & 0x08:
            unmapped.append(read)
        else:
            orientation1 = 'R' if read.flag & 0x10 else 'F'
            orientation2 = 'R' if read.flag & 0x20 else 'F'
            o = orientation1 + orientation2
            if not((o == orientation and read.pos < read.nextPos) or (o == orientation_reversed and read.pos > read.nextPos)):
                bad_orienatation.append(read)
        if read.chrom != read.nextName:
            interchromosomal.append(read)
    return short, long, bad_orienatation, interchromosomal, unmapped

def main():
    split_file_name = sys.argv[1]
    disc_mp_file_name = sys.argv[2]
    mean_mp = int(sys.argv[3])
    sigma_mp = int(sys.argv[4])
    disc_pe_file_name = sys.argv[5]
    mean_pe = int(sys.argv[6])
    sigma_pe = int(sys.argv[7])

    print "Looking for abnormal matepair reads"
    short_mp, long_mp, bad_orienatation_mp, interchromosomal_mp, unmapped = findAbnormalReads(disc_mp_file_name, mean_mp, sigma_mp, 'RF')
    print "abnormal insert size: " + str(len(short_mp)) + str(len(long_mp))
    print "wrong orientation: " + str(len(bad_orienatation_mp))
    print "interchromosomal changes: " + str(len(interchromosomal_mp))

    print "Looking for abnormal pairend reads"
    short_pe, long_pe, bad_orienatation_pe, interchromosomal_pe, unmapped = findAbnormalReads(disc_pe_file_name, mean_pe, sigma_pe, 'FR')
    print "abnormal insert size: " + str(len(short_pe)) + str(len(long_pe))
    print "wrong orientation: " + str(len(bad_orienatation_pe))
    print "interchromosomal changes: " + str(len(interchromosomal_pe))


if __name__ == "__main__":
    sys.exit(main())
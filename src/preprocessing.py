import sys
import sam_fields
import readsam
import otsu

def isSplitRead(samList):
    if 'SA:' in samList[sam_fields.TAGS:]:
        return True
    else:
        return False

def preprocess(file_name, split_file, disc_file):
    insert_sizes = []
    f = readsam.readSamRecords(file_name)
    with open(split_file, 'w') as sf, open(disc_file, 'w') as df:
        for samList in f:
            if isSplitRead(samList):
                sf.write('\t'.join(samList) + '\n')
            else:
                df.write('\t'.join(samList) + '\n')
                insert_sizes.append(abs(int(samList[sam_fields.LEN])))
    return insert_sizes


def main():
    file_name = sys.argv[1]
    mix_reads = bool(sys.argv[2])
    if mix_reads:
        bins = int(sys.argv[3])
    split_file_Name = file_name[0:-4] + "_split.sam"
    disc_file_name = file_name[0:-4] + "_disc.sam"
    insert_sizes = preprocess(file_name, split_file_Name, disc_file_name)
    if mix_reads:
        threshold = otsu.otsu_threshold(insert_sizes, bins)
        print threshold

if __name__ == "__main__":
    sys.exit(main())
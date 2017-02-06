import sam
import os.path

def readSamFile(name):

    samFile = sam.SAM()
    with open(name, 'r') as f:
        line = f.readline()

        # read header
        while line[0] == '@':
            line = f.readline()

        # read rest
        while line!='':
            samList = line.strip().split('\t')
            samFile.addRead(sam.Read(samList))
            line = f.readline()

    return samFile

# generator
def readSamRecords(name):
    with open(name, 'r') as f:
        line = f.readline()

        # read header
        while line[0] == '@':
            line = f.readline()

        # read rest
        while line!='':
            samList = line.strip().split('\t')
            yield samList
            line = f.readline()
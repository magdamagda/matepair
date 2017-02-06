
class Read():

    def __init__(self, samList):
        self.name = samList[0]
        self.flag = int(samList[1])
        self.chrom = samList[2]
        self.pos = int(samList[3])
        self.mapquality = int(samList[4])
        self.cigar = samList[5]
        self.nextName = samList[6]
        self.nextPos = int(samList[7])
        self.templateLength = int(samList[8])
        self.seq = samList[9]
        self.quality = samList[10]
        self.tags = samList[11:]
        self.orientation = None
        self.unmapped = None

class SAM():

    def __init__(self):
        self.reads = []
        self.discordant = []
        self.split = []

    def addRead(self, r):
        self.reads.append(r)

    def deleteReadInPos(self, pos):
        i=0
        while i<len(self.reads):
            r = self.reads[i]
            r_end = r.pos+len(r.seq)
            if r.pos < pos and r_end > pos:
                del self.reads[i]
            else:
                i += 1


    def markAsSplitRead(self, i):
        self.split.append(self.reads[i])

    def markAsDiscordantRead(self, i):
        self.discordant.append(self.reads[i])

    def clear(self):
        del self.reads[:]
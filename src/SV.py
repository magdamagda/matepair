class Evidence():

    def __init__(self):
        self.reads = []
        self.bp_type = None
        self.start = 0
        self.end = 0

class Breakpoint():

    def __init__(self):
        self.pos = 0
        self.type = None
        self.complementary_bp = None

def detectSV(split_reads, pe_short, pe_long, abnormal_orient_pe, mp_short, mp_long, abnormal_orient_mp):
    split_evidences = []
    for r in split_reads:
        split_evidences += evidencesFromSplitRead(r)
    return 0

# for each abnormal read estimate where, breakpoint can be - construct evidences
# start with split reads, that are obvious evidences, find all evidences supporting splitread breakpoint - heuristic
# delete used evidences
# bild a graph(bipartie graph, two sides with the same evidence, connection between evidences voting for other evidence), find min vertex cover using tree decomposition

def evidencesFromSplitRead(read):
    evidences = []
    return evidences
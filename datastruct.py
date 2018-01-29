
class Struct:

    def __init__(self, id, loci):
        self.id = id
        self.loci = loci

    def add_loci(self, locus):
        self.loci = locus

    def get_id(self):
        return self.id

    def get_loci(self):
        return self.loci

    def get_unique(self):
        uniq = set(self.id)
        return uniq
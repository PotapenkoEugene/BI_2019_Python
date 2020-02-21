class Rna():
    def __init__(self, rnaseq: str):
        self.rnaseq = rnaseq.upper()
        from re import match
        if not match(r'^[AUGC]*$', self.rnaseq, ):  # check
            raise TypeError('For input need RNA string object')

    def gc_content(self):
        gc_cont = (self.rnaseq.count('G') + self.rnaseq.count('C')) / len(self.rnaseq)
        return gc_cont

    def reverse_complement(self):
        rev_seq = []
        for i in range(len(self.rnaseq) - 1, -1, -1):
            nucl = self.rnaseq[i]
            if nucl == 'A':
                nucl_out = 'U'
            elif nucl == 'U':
                nucl_out = 'A'
            elif nucl == 'C':
                nucl_out = 'G'
            elif nucl == 'G':
                nucl_out = 'C'
            rev_seq.append(nucl_out)
        return ''.join(rev_seq)

    def __iter__(self):
        return iter(self.rnaseq)

    def __eq__(self, other):
        return isinstance(other, Rna) and self.rnaseq == str(other)

    def __str__(self):
        return self.rnaseq

    def __repr__(self):
        return self.rnaseq

    def __hash__(self):
        return hash(self.rnaseq)


class Dna():

    def __init__(self, dnaseq: str):
        self.dnaseq = dnaseq.upper()
        from re import match
        if not match(r'^[ATGC]*$', self.dnaseq, ):  # check
            raise TypeError('For input need DNA string object')

    def gc_content(self):
        gc_cont = (self.dnaseq.count('G') + self.dnaseq.count('C')) / len(self.dnaseq)
        return gc_cont

    def reverse_complement(self):
        rev_seq = []
        for i in range(len(self.dnaseq) - 1, -1, -1):
            nucl = self.dnaseq[i]
            if nucl == 'A':
                rev_seq.append('T')
            elif nucl == 'T':
                rev_seq.append('A')
            elif nucl == 'C':
                rev_seq.append('G')
            elif nucl == 'G':
                rev_seq.append('C')
        return ''.join(rev_seq)

    def transcribe(self):
        seq = self.dnaseq.replace('T', 'U')
        return Rna(seq)

    def __iter__(self):
        return iter(self.dnaseq)

    def __eq__(self, other):
        return isinstance(other, Dna) and self.dnaseq == str(other)

    def __str__(self):
        return self.dnaseq

    def __repr__(self):
        return self.dnaseq

    def __hash__(self):
        return hash(self.dnaseq)
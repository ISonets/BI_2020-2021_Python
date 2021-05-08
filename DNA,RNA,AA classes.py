####  Classes homework ####

class NuclAcid:  # common for DNA and RNA
    def __init__(self, seq):
        """Class init"""  # init
        letters = {'A', 'C', 'T', 'G', 'U'}
        self.seq = seq.upper()  # to be sure
        self.index = 0
        for i in self.seq:  # check your data
            if 'T' in self.seq and 'U' in self.seq:
                raise ValueError('Wrong sequence: it is impossible to have T and U together in a nucleic acid sequence. Check your data and try again.')
            if i not in letters:
                raise ValueError(self.seq + ' is not a nucleic acid sequence. Perhaps you loaded an amino acid sequence. Try again.')

    def __len__(self):
        """Get the length of the string"""  # length of the sequence
        return len(self.seq)

    def __iter__(self):
        return self

    def __next__(self):  # inspiration from here: https://stackoverflow.com/questions/19151/build-a-basic-python-iterator
        try:
            result = self.seq[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def gc_content(self):  # taken from  my older projects
        """Count GC content of the sequence"""
        gc = 0
        for i in self.seq:
            if i == 'G' or i == 'C':
                gc += 1
        return round(gc / len(self) * 100, 2)
        
class DNA(NuclAcid):
    """A DNA sequence"""
    def __init__(self, seq):
        super().__init__(seq)  # https://docs.python.org/3/library/functions.html#super !!!
        for i in self.seq:
            if i not in {'A', 'C', 'T', 'G'}:
                raise ValueError(self.seq + ' is not a DNA sequence. Check your data and try again.')
    
    def DNA_complement(self):
        """Get the complementary DNA sequence"""
        DNA_compl_rules = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        DNA_bases = list(self.seq)
        DNA_compl = [DNA_compl_rules.get(base) for base in DNA_bases]  # https://www.tutorialspoint.com/python/dictionary_get.htm
        return ''.join(DNA_compl)

    def reverse_complement(self):  # just reverse of the previous function
        """Get the reverse complement of DNA sequence."""
        rev_compl = reversed(self.DNA_complement())  # https://pythonz.net/references/named/reversed/
        return ''.join(rev_compl)

    def DNA_to_RNA_transcription(self):
        """Transcription: get a RNA sequence that is product of the given DNA sequence"""
        transcription_rules = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
        DNA_bases = list(self.seq)
        transcribed = [transcription_rules.get(base) for base in DNA_bases]
        RNA_seq = ''.join(transcribed)
        return RNA(RNA_seq)  # get a new class for the sequence
        
class RNA(NuclAcid):  # almost copypaste of DNA except of U instead of T
    """A RNA sequence"""
    def __init__(self, seq):
        super().__init__(seq)
        for i in self.seq:
            if i not in {'A', 'U', 'G', 'C'}:
                raise ValueError(self.seq + ' is not a RNA sequence. Check your data and try again.')
    
    def RNA_complement(self):
        """Returns the complementary RNA sequence."""
        RNA_compl_rules = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
        RNA_bases = list(self.seq)
        RNA_compl = [RNA_compl_rules.get(base) for base in RNA_bases]
        return ''.join(RNA_compl)
    
    # BONUS: translation! FYI: at this stage it will translate from the start of the sequence, even if AUG is not sequence start.
    
    def RNA_to_protein_translation(self):
        """Translation: get an amino acid sequence based on the given RNA sequence"""
       
        RNA_to_protein_table = {
            'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
            'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
            'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',                 
            'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
            'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
            'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
            'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
            'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
            'UUC':'F', 'UUU':'F', 'UUA':'L', 'UUG':'L',
            'UAC':'Y', 'UAU':'Y', 'UAA':'_', 'UAG':'_',
            'UGC':'C', 'UGU':'C', 'UGA':'_', 'UGG':'W', }
    
        RNA_seq = list(self.seq)
        triplets = [RNA_seq[i:i+3] for i in range(0, len(RNA_seq), 3)]
        protein_seq = ''
        
        for triplet in triplets:
            if RNA_to_protein_table.get(triplet) == "_":  # if stop codon occurs, stop
                return
            else:
                aminoacid = [RNA_to_protein_table.get(triplet) for triplet in triplets]
                protein_seq = ''.join(aminoacid)
        return protein_seq

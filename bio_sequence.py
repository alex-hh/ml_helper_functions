from Bio import pairwise2, SeqIO


def pct_id_align(seq_a, seq_b):
    aln = pairwise2.align.globalxx(seq_a, seq_b, one_alignment_only=True)
    return aln[0][2]/min([len(seq_a), len(seq_b)])

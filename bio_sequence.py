from Bio import pairwise2, SeqIO


def pct_id_align(seq_a, seq_b):
    aln = pairwise2.align.globalxx(seq_a, seq_b, one_alignment_only=True)
    return aln[0][2]/min([len(seq_a), len(seq_b)])

# https://www.biostars.org/p/209383/
def search_fasta(pattern, file_path):
  for record in SeqIO.parse(open(file_path, "rU"), "fasta"):
    chrom = record.id
    for match in re.finditer(pattern, str(record.seq), flags=re.IGNORECASE):
      start_pos = match.start() + 1
      end_pos = match.end() + 1
      print(chrom, '\t', start_pos, '\t', end_pos)

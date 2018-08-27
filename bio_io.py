import numpy as np
from Bio import SeqIO
from Bio.motifs import jaspar

def read_fasta(filepath, output_arr=False):
    names = []
    seqs = []
    seq = ''
    with open(filepath, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                if seq:
                    names.append(name)
                    if output_arr:
                        seqs.append(np.array(list(seq)))
                    else:
                        seqs.append(seq)
                name = line.rstrip('\n')[1:]
                seq = ''
            else:
                seq += line.rstrip('\n')
    if output_arr:
        seqs = np.array(seqs)
    return names, seqs

def output_fasta(names, seqs, filepath='sequences.fa'):
    with open(filepath, 'w') as fout:
        for name, seq in zip(names, seqs):
            fout.write('>{}\n'.format(name))
            fout.write(seq+'\n')
            
def jaspar2dict(motiffile, include_rc=False, pseudocount=0.8):
  motif_dict = {}
  with open(motiffile, 'r') as meme:
    records = jaspar.read(meme, "jaspar")
    for r in records:
      r.pseudocounts = pseudocount
      motif_dict[r.matrix_id] = r

      if include_rc:
        rc = r.reverse_complement()
        rc.pseudocounts = pseudocount
        rc.counts = Bio.motifs.matrix.FrequencyPositionMatrix(r.counts.alphabet, rc.counts)
        motif_dict[r.matrix_id+'-rc'] = rc
  return motif_dict

def jaspar2list(motiffile, include_rc=False, pseudocount=0.8):
  motif_list = []
  with open(motiffile, 'r') as meme:
    records = jaspar.read(meme, "jaspar")
    for r in records:
      r.pseudocounts = pseudocount
      motif_list.append(r)

      if include_rc:
        rc = r.reverse_complement()
        rc.pseudocounts = pseudocount
        rc.counts = Bio.motifs.matrix.FrequencyPositionMatrix(r.counts.alphabet, rc.counts)
        motif_list.append(rc)
  return motif_list

import numpy as np

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

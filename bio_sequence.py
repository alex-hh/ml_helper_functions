import os, subprocess
import glob
import pandas as pd
from Bio import pairwise2, SeqIO
from bio_io import read_fasta, output_fasta

def pct_id_align(seq_a, seq_b):
    """
     Useful note on definitions of sequence identity
     http://lh3.github.io/2018/11/25/on-the-definition-of-sequence-identity
    """
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

def blast_one2many(source_seq, target_seqs, blast_path=''):
    jobid = uuid.uuid4().hex
    query_fa = '/tmp/{}_query.fa'.format(jobid)
    target_fa = '/tmp/{}_target.fa'.format(jobid)
    target_db = '/tmp/{}db'.format(jobid)
    outfile = '/tmp/{}.txt'.format(jobid)
    output_fasta(['n{}'.format(i) for i in range(len(target_seqs))],
               target_seqs,
               target_fa)
    output_fasta(['s0'], [source_seq], query_fa)
    str_cmd = blast_path + 'makeblastdb -dbtype prot -in {} -out {}'.format(target_fa, target_db)
    subprocess.call(str_cmd.split(' '))
    str_cmd = blast_path + 'blastp -query {} -db {}' +\
            ' -num_threads 8 -outfmt 6 -out {} -max_hsps 1 -max_target_seqs {}'
    str_cmd = str_cmd.format(query_fa, target_db, outfile, len(target_seqs))
    subprocess.call(str_cmd.split(' '))
    names = ['qseqid', 'sseqid', 'pident', 'length',
           'mismatch', 'gapopen', 'qstart', 'qend',
           'sstart', 'send', 'evalue', 'bitscore']
    bout = pd.read_csv(outfile, sep='\t', names=names)
    temp_files = glob.glob('/tmp/{}*'.format(jobid))
    for f in temp_files:
      os.remove(f)
    return bout
from bio_encoding import encode_strings

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_snp_flankingseq(dna):
  if type(dna) == np.ndarray:
    dna = encode_strings(dna)
  print(dna[:499] + color.RED + color.BOLD + dna[499] + color.END\
        + color.BLUE + dna[500:] + color.END)

import numpy as np

def reversecomp_dnaarr(dnaarr):
    """
    This is assuming dnaarr shape is n_samples, n_basepairs, input_dim
    """
    arr = np.zeros(dnaarr.shape)
    arr[:,:,:4] = np.rot90(dnaarr[:,:,:4], 2, axes=(2,1))
    arr[:,:,4:] = dnaarr[:,::-1,4:]
    return arr
    
def encode_strings(dnastrs, dims=['A', 'G', 'C', 'T']):
    """
    dnastrs: a list of dnastrings, all of the same length, or a single string
    """
    if type(dnastrs) == str:
        arr = np.zeros((len(dnastrs),4))
        for j, c in enumerate(dnastrs):
          if c in dims:
            arr[j, dims.index(c)] = 1
    else:
        seqlen = len(dnastrs[0])
        arr = np.zeros((len(dnastrs), seqlen, 4))   
        for i, dnastr in enumerate(dnastrs):
            assert len(dnastr) == seqlen
            for j, c in enumerate(dnastr):
              if c in dims:
                arr[i, j, dims.index(c)] = 1
    return arr

def decode_string(dna_arr, dims=['A', 'G', 'C', 'T']):
  dnastr = ''
  for charvec in dna_arr: # iterating over the basepair representations
    charsum = np.sum(charvec)
    assert charsum == 0 or charsum == 1
    if charsum == 0:
        char = 'N'
    else:
        char = dims[np.argmax(charvec)]
    dnastr += char
  return dnastr

def decode_strings(dna_arr, dims=['A', 'G', 'C', 'T']):
  """
  dna_arr: an array of shape (n_samples, n_bp, 4)
  """
  dnastrs = []
  for i in range(dna_arr.shape[0]):
    dnastr = ''
    for charvec in dna_arr[i]: # iterating over the basepair representations
      charsum = np.sum(charvec)
      assert charsum == 0 or charsum == 1
      if charsum == 0:
        char = 'N'
      else:
        char = dims[np.argmax(charvec)]
      dnastr += char
    dnastrs.append(dnastr)
  return dnastrs

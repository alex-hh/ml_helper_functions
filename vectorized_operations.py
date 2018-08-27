import numpy as np


def matrix_cosine_sims(M1, M2):
    """
    Compute the pairwise cosine distances between the rows 
    of M1 and those of M2
    """
    dp_mat = np.dot(M1, M2.T)
    norm1 = norm(M1, axis=1)
    norm2 = norm(M2, axis=1)
    
    norm1_tiled = np.tile(np.reshape(norm1, (len(norm1),1)), (1, len(norm2)))
    norm2_tiled = np.tile(np.reshape(norm2, (1, len(norm2))), (len(norm1), 1))
    
    denominators = norm1_tiled * norm2_tiled
    
    return dp_mat / denominators

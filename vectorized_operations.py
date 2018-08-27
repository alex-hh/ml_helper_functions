import numpy as np
from numpy.linalg.linalg import norm


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

# N.B. these are assuming data with batch, len, feats dimensions (i.e. sequential data)
def np_cross_entropy(targets, preds, epsilon=1e-12):
    # at each nucleotide we want to effectively dot product the target aa vector and the log probs
    preds = np.clip(preds, epsilon, 1-epsilon)
    masked_probs = targets * np.log(preds)
    return -np.sum(masked_probs, axis=(1,2))

def np_elbo(z_mean, z_var, targets, preds, log_var=False, epsilon=1e-12):
    return np_kl_loss(z_mean, z_var) + np_cross_entropy(targets, preds)

def np_kl_loss(z_mean, z_var):
    return - 0.5 * np.sum(1 + np.log(z_var+1e-8) - z_var - np.square(z_mean), axis=-1)

# def np_logvar_kl
# TODO define logvar loss to be used in delta_elbo

def np_klstd_loss(z_var):
    return - 0.5 * np.sum(1 + np.log(z_var + 1e-8) - z_var, axis=-1)

def np_klmu_loss(z_mean):
    return 0.5 * np.sum(np.square(z_mean), axis=-1)

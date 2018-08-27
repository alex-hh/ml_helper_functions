import numpy as np


def batched_predict(model, generator):
    """ this is to get around the issues i've found with keras evaluate_generator
    (and the absence of a corresponding predict_generator)
    
    generator should stop iteration after cycling once through all datapoints
    the last generator output will be a batch of 'leftovers' likely of different size to rest
    """
    multi_output = type(model.output_shape) == list
    if multi_output:
        outputs = [[] for o in model.output_shape]
    else:
        outputs = []
    j = 0
    for x_batch, _ in generator:
        
        # if j % 100 == 0:
            # print(j)
        preds = model.predict(x_batch)
        if multi_output:
            for i, o in enumerate(preds):
                outputs[i].append(o)
        else:
            outputs.append(preds)
        j+=1
    if multi_output:
        outputs = [np.concatenate(o) for o in outputs]
    else:
        outputs = np.concatenate(outputs)
    return outputs

def batched_score(model, generator, score_funcs):
    """
    TODO: might be worth redoing this and either 
     1. defining generator within here to allow for handling of leftovers
     2. modifying generator so that it outputs a final batch of a different size to the others
     3. defining aa accuracy within the tensorlow graph (then wouldn't need to iterate through data more than once)
     Returns per sequence scores
    """
    scores = [[] for f in score_funcs]
    for x_batch, targets_batch in generator:
        
        # if j % 100 == 0:
            # print(j)
        preds = model.predict(x_batch)
        for i, f in enumerate(score_funcs):
            scores[i].append(f(targets_batch, preds))
    
    scores = [np.concatenate(s) for s in scores]
    return scores

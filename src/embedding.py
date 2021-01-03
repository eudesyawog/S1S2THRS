import numpy as np
from src.utils import get_batch, get_iteration
from tqdm import tqdm 

def getEmbedding (model,test_S1,test_S2,test_MS,test_Pan,test_y,batch_size,checkpoint_path,embedding_path,lst_sensor,tqdm_display) :
    '''
    Load weights for best configuration and Get Embedding of test set
    '''
    model.load_weights(checkpoint_path)
    print ('Weights loaded')

    iteration = get_iteration(test_y,batch_size)
    print (f'Test batchs: {iteration}')

    embedding = []

    if len(lst_sensor) == 3 :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_s1 = get_batch (test_S1,batch,batch_size)
            batch_s2 = get_batch (test_S2,batch,batch_size)
            batch_ms = get_batch (test_MS,batch,batch_size)
            batch_pan = get_batch (test_Pan,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_s1,batch_s2,batch_ms,batch_pan)
            del batch_s1,batch_s2,batch_ms,batch_pan
            embedding.append(batch_embedding)

    elif len(lst_sensor) == 2 and 's1' in lst_sensor and 's2' in lst_sensor :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_s1 = get_batch (test_S1,batch,batch_size)
            batch_s2 = get_batch (test_S2,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_s1,batch_s2)
            del batch_s1,batch_s2
            embedding.append(batch_embedding)
    
    elif len(lst_sensor) == 2 and 's2' in lst_sensor and 'spot' in lst_sensor :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_s2 = get_batch (test_S2,batch,batch_size)
            batch_ms = get_batch (test_MS,batch,batch_size)
            batch_pan = get_batch (test_Pan,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_s2,batch_ms,batch_pan)
            del batch_s2, batch_ms, batch_pan
            embedding.append(batch_embedding)
    
    elif len(lst_sensor) == 1 and 's1' in lst_sensor :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_s1 = get_batch (test_S1,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_s1)
            del batch_s1
            embedding.append(batch_embedding)
    
    elif len(lst_sensor) == 1 and 's2' in lst_sensor :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_s2 = get_batch (test_S2,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_s2)
            del batch_s2
            embedding.append(batch_embedding)
    
    elif len(lst_sensor) == 1 and 'spot' in lst_sensor :
        for batch in tqdm(range(iteration),disable=not(tqdm_display)):
            batch_ms = get_batch (test_MS,batch,batch_size)
            batch_pan = get_batch (test_Pan,batch,batch_size)
            batch_embedding = model.getEmbedding(batch_ms,batch_pan)
            del batch_ms, batch_pan
            embedding.append(batch_embedding)

    embedding = np.vstack(embedding)
    np.save (embedding_path,embedding)
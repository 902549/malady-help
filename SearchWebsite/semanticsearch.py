import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, util
import os

import pandas as pd


# cwd = os.getcwd()

#Importig the csv
df = pd.read_csv('SearchWebsite/Database_new.csv', index_col = 0)
corpus = df['Data'].tolist()
labels = df['Label'].tolist()



#Fetches the disease data
def fetch_disease_info(dataframe_idx):
    info = df.iloc[dataframe_idx]
    meta_dict = dict()
    meta_dict['Title'] = info['Title']
    meta_dict['Disease'] = info['Label']
    meta_dict['Data'] = info['Data'][:500]
    meta_dict['Source'] = info['Source']
    return meta_dict
    
#Main search which returns the results    
def search(query, top_k, index, model):
    t=time.time()
    query_vector = model.encode([query])
    top_k = index.search(query_vector, top_k)
    print('>>>> Results in Total Time: {}'.format(time.time()-t))
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    results =  [fetch_disease_info(idx) for idx in top_k_ids]
    return results

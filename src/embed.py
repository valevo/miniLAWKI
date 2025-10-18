from sentence_transformers import SentenceTransformer

import numpy as np
import pandas as pd

import torch

from tqdm import tqdm
import csv

# out_dir = "./outputs/2025-03-04T18:07"

# model = "nomic-ai/nomic-embed-text-v1"
# model = "BAAI/bge-m3-unsupervised"
model_str = 'paraphrase-multilingual-mpnet-base-v2'
# model_str = 'paraphrase-multilingual-MiniLM-L12-v2'
# model = 'distiluse-base-multilingual-cased-v2 '


model = SentenceTransformer(model_str, trust_remote_code=True)


def embed(lawki_dir, return_embeddings=True, save_embeddings=True):

    meta = pd.read_csv(f"{lawki_dir}/metadata.csv", lineterminator="\n")#.iloc[:300]
    
    dim = next(model.parameters()).shape[1]
    print(f"embedding dimensionality = {dim}")
    chunk_size = min(len(meta), 7)
    
    embs = np.zeros((meta.shape[0], dim))
    cur_ind = 0
    # for i, txt in tqdm(enumerate(meta.pretty_text), total=meta.shape[0]):
    chunks = np.array_split(list(meta.pretty_text), int(len(meta)/chunk_size))
    for txts in tqdm(chunks, total=len(chunks)):
        try:
            cur_emb = model.encode(txts)
            embs[cur_ind:cur_ind+len(txts)] = cur_emb
            
        except TypeError as e:
            print(f"TYPEERROR: {e}\n\tsentence = {s}")
            embs[cur_ind:cur_ind+len(cur_emb)] = np.zeros((len(txts), dim))
        
        cur_ind = cur_ind+len(cur_emb)

    if save_embeddings:
        # np.savetxt(f"{lawki_dir}/embeddings_{model_str.replace("/", "")}.tsv", embs, delimiter="\t")

        embs_df = pd.DataFrame(embs, index=meta.link)
        embs_df.to_csv(f"{lawki_dir}/embeddings_{model_str.replace("/", "")}.csv")

    if return_embeddings:
        return embs
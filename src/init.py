from tqdm import tqdm
from glob import glob

from datetime import datetime
import os
import sys

import pandas as pd
import numpy as np
import csv

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound
## SET UP ENV

from parameters import *
    

def main(terms, overwrite=True):
    
    ### TRANSLATE
    
    print("\n=========================\n" + 
          f"1. TRANSLATING TERMS {terms}")
          
    translators = [GoogleTranslator(source='en', target=l) for l in langs]
    
    # trans_d = {t: {l: g.translate(t) for l, g in zip(langs, translators)} 
    #          for t in tqdm(terms)}

    trans_d = {}
    for t in tqdm(terms):
        cur_d = {}
        for l, g in zip(langs, translators):
            try:
                cur_d[l] = g.translate(t)
            except TranslationNotFound:
                continue
        trans_d[t] = cur_d
    
    
    
    ### CREATE DATAFRAME
    
    records = [dict(topic=to, language=l, term=te, platform=pl, link="_") #, link_nr=i) 
               for to, topic_dict in trans_d.items()
               for l, te in topic_dict.items() 
               for pl in platforms.keys()
                for _ in range(num_links)]
    
    records.extend(dict(topic=to, language="en", term=to, platform=pl, link="_")
                  for to, _ in trans_d.items()
                  for pl in platforms.keys()
                  for _ in range(num_links))
    
    df_terms = pd.DataFrame.from_records(records)
    df_terms = df_terms.applymap(lambda s: s.replace("\n", ""))
    df_terms = df_terms[df_terms.topic.str.len() > 0]
    df_terms = df_terms[df_terms.term.str.len() > 0]
    df_terms.to_csv(f"{lawki_dir}/terms.csv", sep=",", quoting=csv.QUOTE_ALL, quotechar='"', index=False)
    
    print("\n=========================\n")

    print("\n=========================\n" + 
          "2. SCRAPING LINKS")
    from scrape_links import scrape_links
    
    scrape_links(lawki_dir)
    
    print("\n=========================\n")
    
    print("\n=========================\n" + 
          "2. SCRAPING METADATA")
    from scrape_metadata import scrape_metadata
    
    scrape_metadata(lawki_dir)
    print("\n=========================\n")
    

    print("\n=========================\n" + 
          "3. SCRAPING VIDEOS")
    from scrape_videos import scrape_videos
    
    scrape_videos(lawki_dir)
    print("\n=========================\n")


    print("\n=========================\n" + 
          "4. ALIGNING EVERYTHING")
    # align everything
    meta = pd.read_csv(f"{lawki_dir}/metadata.csv", lineterminator="\n").set_index("link")
    with open(f"{lawki_dir}/downloaded.txt") as handle:
        dwnld = [l.split()[1] for l in handle.readlines()]
    vids = glob(f"{lawki_dir}/videos/*")
    vids = pd.Series(vids).apply(lambda s: s.split("/")[-1].split(".")[0])
    
    meta2 = meta.loc[meta.index.intersection(vids)]
    meta2.reset_index().to_csv(f"{lawki_dir}/metadata.csv", index=False)
    meta.reset_index().to_csv(f"{lawki_dir}/metadata_original.csv", index=False)
    print("\n=========================\n")

    print("\n=========================\n" + 
          "5. EMBEDDING METADATA")
    from embed import embed
    
    embed(lawki_dir)

    print("\n=========================\n")



if __name__ == "__main__":
    lawki_name, overwrite, *_ = sys.argv[1:]

    if not lawki_name:
        lawki_name = datetime.today().strftime("%Y-%m-%dT%H:%M")
    lawki_dir = f"outputs/{lawki_name}"
    
    if os.path.isdir(lawki_dir) and overwrite.lower().startswith("n"):
        exit()
    os.makedirs(lawki_dir, exist_ok=True)

    ### PARAMETERS
    
    with open(f"./inputs/{lawki_name}.txt") as handle:
        terms = [l.strip() for l in handle.readlines() if l]

    
    main(terms, overwrite=overwrite)
    
    print("\n===================================", flush=True)
    print(f"DONE WITH {lawki_dir}")
    with open(f"{lawki_dir}/FINISHED", "w") as handle:
        handle.write("finished at " + datetime.today().strftime("%Y-%m-%dT%H:%M:%S"))
    print("===================================", flush=True)


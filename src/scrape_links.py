from tqdm import tqdm
from selenium import webdriver

import csv
import pandas as pd

from parameters import *
from utils import get_links


def scrape_links(lawki_dir, return_links=True, save_links=True):
    df = pd.read_csv(f"{lawki_dir}/terms.csv")
    df = df.set_index(["language", "term", "platform"]).sort_index()
    
    
    
    with webdriver.Firefox() as driver:
        for i, (cur_lang, cur_term, cur_platform) in enumerate(tqdm(df.index.drop_duplicates())):
            # cur_sub = df.loc[(cur_lang, cur_term, cur_platform)]
            # links_scraped = df.loc[(cur_lang, cur_term, cur_platform), "link"].str.len() > 1
            # print(links_scraped.sum())
            # if links_scraped.all():
            #     print(f"row {i} done, skipping", flush=True, end="...\n")
            #     continue 
        
            links = get_links(driver=driver, platform=cur_platform, term=cur_term, n=5)
            links = [l[:11] for l in links]
    
            links = links + [None]*num_links
            df.loc[(cur_lang, cur_term, cur_platform), "link"] = links[:num_links]
            df.loc[(cur_lang, cur_term, cur_platform), "done"] = True

    if save_links:
        df.reset_index().to_csv(f"{lawki_dir}/links.csv",  quotechar='"', quoting=csv.QUOTE_ALL, index=False)
    if return_links:
        return df


import sys

if __name__ == "__main__":
    lawki_dir = sys.argv
    
    print(f"Scraping links for LAWKI {lawki_dir}", flush=True)

    scrape_links(lawki_dir, return_links=False)
    
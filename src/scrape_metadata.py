from __future__ import unicode_literals
import youtube_dl
import yt_dlp as youtube_dl

from time import time
from tqdm import tqdm
from glob import glob

import pandas as pd

from youtube_dl import DownloadError

import pickle

from joblib import Parallel, delayed


def yt_expand(_id): return f"https://www.youtube.com/watch?v={_id}"
def dm_expand(_id): return f"https://www.dailymotion.com/video/{_id}"
            
            
def get_row(row):
    with youtube_dl.YoutubeDL(dict(quiet=True, verbose=False, ignoreerrors=True)) as ydl:
        expand = yt_expand if row.platform == "youtube" else dm_expand
        u = expand(row.link)


        try:
            dictMeta = ydl.extract_info(
                                u,
                            download=False)

            if dictMeta is None:
                print(f"download didn't return with {u=}")
                return dict(link=row.link)

            categories = dictMeta.get("categories", [None])[0]
            tags = tuple(dictMeta["tags"])
            select_meta = dict(
                    link=dictMeta["id"],

                    channel=dictMeta["channel"] if "channel" in dictMeta else None,
                    title=dictMeta["title"],
                    description=dictMeta["description"],

                    date=dictMeta["upload_date"], # if "upload_date" in dictMeta else dictMeta["timestamp"],
                    views=dictMeta["view_count"],
                    duration=dictMeta.get("duration", None), # if "duration" in dictMeta else None,

                    tags=tags, 
                    categories=categories,

                    age_limit=dictMeta["age_limit"],
    #                 average_rating=dictMeta["average_rating"],
                    like_count=dictMeta["like_count"] if "like_count" in dictMeta else None,
    #                 dislike_count=dictMeta["dislike_count"],
                )

            return select_meta

        except DownloadError as e:

            print(e, "\n", u)
            return dict(link=row.link)
            
            
            
def scrape_metadata(lawki_dir, return_metadata=True, save_metadata=True):    
    links = pd.read_csv(f"{lawki_dir}/links.csv").dropna(subset=["link"])
            
    dicts = Parallel(n_jobs=8, backend="loky")(delayed(get_row)(r) 
                                               for i, r in tqdm(links.iterrows(), 
                                                                total=links.shape[0]))

    # with open("./metadata_dicts.pkl", "wb") as handle:
    #     pickle.dump(dicts, handle)




    meta_df = pd.DataFrame.from_records(dicts).set_index("link")
    meta_df = meta_df.dropna(subset=["duration"])
    
    links = pd.read_csv(f"{lawki_dir}/links.csv").set_index(["language", "term", "platform"])
    # actual = glob(f"{lawki_dir}/videos/*.mp4")
    # actual = set(actual)

    def merge_text(row):
        return (row.title if isinstance(row.title, str) else ""), \
                (row.description if isinstance(row.description, str) else ""), \
                (row.channel if isinstance(row.channel, str) else ""), \
                (", ".join(row.tags) if isinstance(row.tags, list) else "")
    
    
    def pretty_text(row):
        t, d, c, tgs = merge_text(row)
        return f"Title: {t}\n\nChannel: {c}\n\nDescription: {d}\n\n{tgs}"
    
    
    meta_df.loc[:, "text"] = meta_df.apply(lambda r: "".join(merge_text(r)), axis="columns")
    meta_df.loc[:, "pretty_text"] = meta_df.apply(pretty_text, axis="columns")
    

    keep = ((meta_df.text.str.len() > 20) & (meta_df.duration < 1200) &\
            (meta_df.isna().sum(1) < 3) & ~(meta_df.views.isna()))
    print(f"\tkeeping {keep.sum()} out of {len(meta_df)} records ({round(keep.sum()/len(meta_df), 3)}%)")
    final_df = meta_df[keep].copy(deep=True)
    
    # do some transformations
    import datetime
    final_df.loc[:, "date"] = pd.to_datetime(final_df.date)
    final_df.loc[:, "recency"] = (pd.to_datetime("today") - final_df.date).apply(lambda d: d.days)


    df2 = links.reset_index()
    df2 = df2[["link", "language", "term", "platform"]].set_index("link")
    
    # common = set(final_df.index) & set(df2.index)
    # common = [l for l in final_df.index if l in common]
    
    # df2 = df2.loc[common]
    # final2 = final_df.loc[common]
    
    meta = df2.merge(final_df, left_index=True, right_index=True)
    meta = meta.reset_index().drop_duplicates(subset=["link"])

    if save_metadata:
        meta.to_csv(f"{lawki_dir}/metadata.csv", index=False)
    if return_metadata:
        return meta


import sys

if __name__ == "__main__":
    lawki_dir = sys.argv
    
    print(f"Scraping metadata for LAWKI {lawki_dir}", flush=True)

    scrape_metadata(lawki_dir, return_links=False)

import yt_dlp as youtube_dl

import numpy as np
import pandas as pd

from tqdm import tqdm
from time import time
import os
from glob import glob


def live_hook(d):
#     print("\n\n\n", d.keys(), d["duration"], "\n\n\n")
#     print(d["playlist"])
#     print(d["playlist_index"])
    
    if d["duration"] > 200:
        return f"duration > 200 (is {d['duration']})"
        
    if d["is_live"]:
        return "is_live"
    return None


def yt_expand(_id): return f"https://www.youtube.com/watch?v={_id}"
def dm_expand(_id): return f"https://www.dailymotion.com/video/{_id}"

def download(url_ls, prog):
    def u_pbar(d):
        if d["status"] == "downloading":
            prog.set_description(f"{d['filename']}: {d['_percent_str']} ({d['_speed_str']})")
        elif d["status"] == "finished":
            prog.update(1)
        else:
            return ValueError()

    ydl_opts = {
            'progress_hooks': [u_pbar],
            'quiet': True,
            'verbose': False,
            "writesubtitles": True,
            "subtitleslangs": "en",
            "subtitlesformat": "srt",
            "writethumbnail": False, #True,

            "download_archive": "downloaded.txt",

            "ignoreerrors": True,
            "outtmpl": "videos/%(id)s.%(ext)s",
        
            # "format": "best",
            "socket_timeout": 1,
            "match_filter": live_hook
        }
        
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_ls)






# feature_dir = "../features"

# links = pd.read_csv(f"{feature_dir}/features.csv")
# links = links.sort_values(by="link")


# new_durs = pd.read_csv("redownloaded_durations.csv")
# new_durs = new_durs.sort_values(by="id")

# links['duration'] = new_durs['duration']


# # filter and schedule

# links = links.dropna()
# links = links[links.duration <= 1000]
# scheduled = links.sample(frac=1.0, weights=1/(links.duration**2))

def clean_up():
    # remove .part files
    # delete files that are not part of "downloaded.txt"
    with open("downloaded.txt") as handle:
        dwnld = [l.split()[1] for l in handle.readlines()]

    for f in glob("videos/*"):
        if not any((d in f) for d in dwnld):
            print(f"FILE {f} to be deleted!")
            os.remove(f)

    for f in glob("videos/*"):
        parts = f.split(".")
        if len(parts) > 2 and parts[1].startswith('f'):
            print(f"FILE {f} to be deleted!")
            os.remove(f)




def scrape_videos(lawki_dir):
    orig_dir = os.getcwd()
    os.chdir(lawki_dir)


    videos = pd.read_csv("./metadata.csv")
    # shuffled = videos.iloc[np.loadtxt("links_perm_inds.txt").astype("int")]
    # videos = videos[videos.link != ""]
    # NOT NEEDED
    # videos = videos[videos.link.notna()].drop_duplicates(subset=["link"])
    
    print(f"total of {videos.shape[0]} videos to be downloaded")
    
    urls = [yt_expand(row.link) if row.platform == "youtube" else dm_expand(row.link)
               for i, row in videos.iterrows()]

    pbar = tqdm(total=len(urls))    
    download(urls, pbar)

    clean_up()
    
    os.chdir(orig_dir)


import sys

if __name__ == "__main__":
    lawki_dir = sys.argv
    print(f"Scraping videos for LAWKI {lawki_dir}", flush=True)
    
    scrape_videos(lawki_dir)    
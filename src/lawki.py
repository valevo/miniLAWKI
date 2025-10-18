from tqdm import tqdm

import os
from glob import glob
import pandas as pd

from parameters import *
from rw import NeighbourRW

from moviepy.editor import VideoFileClip, concatenate_videoclips
# from moviepy import VideoFileClip, concatenate_videoclips
import seaborn as sns

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


if __name__ == "__main__":
    import sys
    lawki_name, *_ = sys.argv[1:]

    lawki_dir = "outputs/"+lawki_name

    # orig_dir = os.getcwd()
    # os.chdir(lawki_dir)
    # clean_up()
    # os.chdir(orig_dir)
    # # align everything
    # meta = pd.read_csv(f"{lawki_dir}/metadata.csv", lineterminator="\n").set_index("link")
    # with open(f"{lawki_dir}/downloaded.txt") as handle:
    #     dwnld = [l.split()[1] for l in handle.readlines()]
    # vids = glob(f"{lawki_dir}/videos/*")
    # vids = pd.Series(vids).apply(lambda s: s.split("/")[-1].split(".")[0])

    # meta = meta.loc[meta.index.intersection(vids)]
    
    # from embed import embed
    # if not os.path.isfile(f"{lawki_dir}/embeddings_paraphrase-multilingual-mpnet-base-v2.csv"):
    #     embed(lawki_dir)

# lawki_dir = "outputs/full_test/"

    meta = pd.read_csv(f"{lawki_dir}/metadata.csv").set_index("link")
    space = pd.read_csv(f"{lawki_dir}/embeddings_paraphrase-multilingual-mpnet-base-v2.csv").set_index("link")
    space = space.loc[meta.index].values
    
    
    def file_from_link(files, link):
        matches = [f for f in files if link in f]
        if not matches:
            return None
            # raise ValueError(f"{link} not in {files}!")
        return matches[0]
    
    video_files = glob(f"{lawki_dir}/videos/*")
    

    rw = NeighbourRW(n_neighbours=2, space=space, meta=meta)
    
    steps = []
    for _ in range(15):
        try:
            i, cur_row, (start, duration) = rw.step(0)
            steps.append([cur_row.name, start, duration])
        except ValueError:
            print("DONE!")
            break
    
    steps = pd.DataFrame(steps, columns=["link", "start", "duration"])

    print(f"{steps.duration.sum()/60=}", flush=True)
    
    
    clips = [(file_from_link(video_files, l), s, d)
            for i, (l, s, d) in steps.iterrows()]
    clips = [VideoFileClip(l).subclip(s, s+d)
             for l, s, d in tqdm(clips, desc="loadig VideoFileClips") if l]

    print([v.duration for v in clips], meta.loc[steps.link].duration, flush=True)


    
    final = concatenate_videoclips(clips, method='compose').set_fps(24)

    print(f"{final.duration=}, {final.fps=}")
    final.write_videofile(f"{lawki_dir}/lawki.mp4") 


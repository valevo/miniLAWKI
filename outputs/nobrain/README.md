# THIS IS THE OUTPUT OF A LAWKI PROCESS 

The LAWKI video outcome are lawki.mp4, lawki1.mp4, etc. There is no particular order to these files, as they are each outcomes of the same random walk with the same inputs. (Please contact me if you'd like more LAWKI videos.)

The other relevant data to the LAWKI process (which lead to the lawki.mp4 files) are in .csv files in this directory; they can be opened with Microsoft Excel or Google Sheets or similar software for inspection and use.

## terms.csv

Contains the translations of the original input terms (together with language codes for the respective language codes,
"ar" is Arabic, "zh-CN" is Chinese, etc). The columns "platform" and "link" are placeholders for later
scraping of links of videos.

## links.csv

The same as "terms.csv" but now with the links filled in. E.g. "hVYf-saY0AU" is the suffix for the YouTube
URL "https://www.youtube.com/watch?v=hVYf-saY0AU". 

## metadata.csv

Has the metadata of the YouTube (and Dailymotion) videos, such as title, description, view count, etc. The difference between metadata and metadata_original is that metadata_original may contain rows for videos that were either not actually downloaded (failed) or for some other reason not usable. So metadata.csv is the definitive file for the videos in the lawki.mp4 outcome.

## embeddings_paraphrase-multilingual-mpnet-base-v2.csv

Is the vector space with embeddings.


## Running Instructions

The below process requires a Python (tested on 3.13) environment with additional libraries installed.

To make `mini_LAWKI` with each of the files in `inputs`, run:

 - `init_all.sh`: calls `src/init.py` with (1) folder name and (2) "yes" for each name in `inputs` 
   (skips if the folder name with file FINISHED in it already exists in `outputs`)
 - `lawki_all.sh`: calls `src/lawki.py` with folder name for each name in `inputs`
   (skips if the folder name isn't already in `outputs` (i.e. is hasn't been initialised with `init.py`)
   or `lawki.mp4` already exists)

After these scripts are (successfully) done, look in `outputs` for your mini_LAWKI.

### Scripts

The processes above (`init` and `lawki`) use the following scripts, they are all contained in `src/`:
   - `init.py`
   - `scrape_links.py`
   - `scrape_metadata.py`
   - `scrape_videos.py`
   - `embed.py`
   - `lawki.py`
   - `parameters.py`: contains the parameters for mini_LAWKI (set of languages, 
     number of videos to download, etc) -- imported by `init.py` and `lawki.py`
   - `rw.py`
   - `utils.py`
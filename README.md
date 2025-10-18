# Instructions

To make `mini_LAWKI` with each of the folders in `inputs`, run:

 - `init_all.sh`: calls `src/init.py` with (1) folder name and (2) "yes" for each name in `inputs` 
   (skips if the folder name with file FINISHED in it already exists in `outputs`)
 - `lawki_all.sh`: calls `src/lawki.py` with folder name for each name in `inputs`
   (skips if the folder name isn't already in `outputs` (i.e. is hasn't been initialised with `init.py`)
   or `lawki.mp4` already exists)

After these scripts are (successfully) done, look in `outputs` for your mini_LAWKI.

## Scripts

 - `src/` is the folder which contains all code to run mini_LAWKI:
   - `init.py`: 
   - `lawki.py`:
   - `parameters.py`: contains the parameters for mini_LAWKI (set of languages, 
     number of videos to download, etc) -- imported by `init.py` and `lawki.py`
   - `  



## TODO

 - load translations if they already exist (table `terms.csv`)
 - input terms seem to be loaded with trailing `\n`

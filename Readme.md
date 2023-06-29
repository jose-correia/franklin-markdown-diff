# franklin-markdown-diff

This script can be used to compare a large set of Franklin URLs.
The objective is to make it easier to detect differences between older and newer versions of the same assets.


## Approach
The script will iterate through each url and open a new browser window showing the Markdown differences between both the paths.

After verifying the differences, one must press `ENTER` for the script to continue to the next path.

## Usage
1. Add all the urls for the original version of the assets in urls.txt
2. Install requirements

```bash
pip3 install ghdiff
```

3. Edit the `BASE_PATH` and the `TEMPORARY_FILES_SUBPATH` variables in `main.py`

3. Run script
   
```bash
python3 -m main
```

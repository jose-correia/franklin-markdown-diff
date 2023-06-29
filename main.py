# This script can be used to fetch all the Markdown files under a given
# directory of a website and compare them with the files that have the
# same name under another directory. If there are any differences,
# the script will print out the file names and the differences.

import os
import requests
import ghdiff
import webbrowser


BASE_PATH = 'https://main--moleculardevices--hlxsites.hlx.page'
TEMPORARY_FILES_SUBPATH = '/drafts'

# This method gets a list of subpaths to be compared,
# from the urls.txt file
def get_subpaths():
    subpaths = []
    with open('urls.txt', 'r') as f:
        for line in f:
            # get the path after /drafts
            subpath = line.strip().split('/drafts')[1]
            subpaths.append(subpath)
    return subpaths

# This method receives a subpath and uses it to perform a request
# to the website to retrieve the .md file content
def get_markdown_content(path):
    url = path + '.md'
    response = requests.get(url)

    # if response code is 404, return an empty string
    if response.status_code == 404:
        raise Exception('File not found: ' + url)
    
    return response.text

def get_original_path(subpath):
    return BASE_PATH + subpath

def get_new_path(subpath):
    return BASE_PATH + TEMPORARY_FILES_SUBPATH + subpath

# This method opens the diff in the browser
def open_diff(subpath, diff):
    path = os.path.abspath('temp.html')
    url = 'file://' + path

    # Add 2 paragraphs containing the original path and the new path
    # This paragraphs are added to the <div class="diff"> element
    original_path = get_original_path(subpath)
    new_path = get_new_path(subpath)
    diff = diff.replace(
        '<div class="diff">',
        '<div class="diff"><p>Original path: <a href="' + original_path + '">' + original_path + '</a></p><p>New path: <a href="' + new_path + '">' + new_path + '</a></p>',
    )

    with open(path, 'w') as f:
        f.write(diff)

    webbrowser.open(url)

def main():
    subpaths = get_subpaths()
    for subpath in subpaths:
        # get the content of the .md file under /
        current_version_path = BASE_PATH + subpath
        # get the content of the .md file under /drafts
        new_version_path = BASE_PATH + TEMPORARY_FILES_SUBPATH + subpath
        
        try:
            current_version_markdown = get_markdown_content(current_version_path)
            new_version_markdown = get_markdown_content(new_version_path)
        except Exception as e:
            print(e)
            continue

        # compare the two files
        print('Comparing ' + subpath + '...')
        diff = ghdiff.diff(current_version_markdown, new_version_markdown)

        open_diff(subpath, diff)

        # wait for user input to continue
        input('Press ENTER to continue to next path...')

if __name__ == '__main__':
    main()
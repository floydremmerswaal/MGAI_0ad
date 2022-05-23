# importing the requests module
import os
import requests
from tqdm import tqdm


download_dest_path = '0ad-master/master.zip'
# Check if file exists
if not os.path.exists(download_dest_path):
    print('Download started')
    url = 'https://github.com/0ad/0ad/archive/refs/heads/master.zip'

    # Downloading the file by sending the request to the URL
    def download(url: str, fname: str):
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get('content-length', 0))
        # Can also replace 'file' with a io.BytesIO object
        with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    
    os.makedirs('0ad-master', exist_ok=True)

    download(url, download_dest_path)

    print('Download Completed')
else:
    print('File already exists, skipping download')

print('Unpacking zip')
import zipfile
#unpack the zip file
with zipfile.ZipFile(download_dest_path, 'r') as zip_ref:
    for file in zip_ref.namelist():
        if file.endswith('.xml'):
            zip_ref.extract(file, '0ad-master/')
    # zip_ref.extract('0ad-master/binaries/data/mods/public/simulation/templates/*', '0ad-master/templates')

from distutils.dir_util import copy_tree
copy_tree("0ad-master/0ad-master/binaries/data/mods/public/simulation/templates", "0ad-master/templates")

import shutil
shutil.rmtree('0ad-master/0ad-master')

print('Generating entity list')
# get the path to the templates directory
templates_path = os.path.join(os.path.dirname(__file__), '../', '0ad-master/templates')

files_names = []
# recursively walk the templates directory
for root, dirs, files in os.walk(templates_path):
    # for each file in the directory
    for filename in files:
        if "template_" in filename:
            continue
        if "cached" in filename:
            continue
        # get the path to the file
        # append parent directories to the path
        # remove substring from root to get the path relative to the templates directory
        
        file_path = os.path.join(root, filename)
        file_path = file_path.replace(templates_path +"\\", '').replace('.xml', '')
        # append the path to the list
        files_names.append(file_path)
        
# write the list to a text file
with open('pcg/entities.py', 'w') as f:
    for item in files_names:
        py_var = item.replace('\\', '__')
        py_name = item.replace('\\', '/')
        f.write(f"{py_var} = \"{py_name}\"\n")

print('All done!')
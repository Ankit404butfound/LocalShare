from bs4 import BeautifulSoup
from urllib.parse import unquote

import requests
import os
  
URL = "http://192.168.0.156:8000"
files = 0
folders = 0


IGNORE_DIR = ["Work/", "$RECYCLE.BIN", "__pycache__/", "appdata/", "libs/", "SmartClassDesktop/", "UBUNTU/"]
DOWNLOAD_DIR = "D/"


def download_file(url):
    local_filename = DOWNLOAD_DIR+url.split(':8000/')[-1]
    if os.path.exists(DOWNLOAD_DIR+url.split(':8000/')[-1]):
        print("File exists", DOWNLOAD_DIR+url.split(':8000/')[-1])
        return
    print("Downloading", local_filename)
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
    except Exception as e:
        file = open("log.txt", "w", encoding="utf-8")
        file.write(str(e))
        file.close()
##    return local_filename


def downloadAndFind(url):
    global files, folders
    try:
        dir_path = url.split(":8000/")[1]
    except:
        dir_path = ""
##    print(dir_path)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    elements = soup.findAll("li")

    for ignore_dir in IGNORE_DIR:
        if ignore_dir in unquote(url):
            print("Ignoring", url)
            return
    
    for element in elements:
        path = element.find("a", href=True)["href"]
        path = unquote(path)
        
        abs_path = f"{url}/{path}" if url[-1] != "/" else f"{url}{path}"
        abs_path = unquote(abs_path)
        
        if "/" in path:
            try:
                os.makedirs(DOWNLOAD_DIR+dir_path)
            except:
                pass
            downloadAndFind(abs_path)
            folders += 1
        else:
            files += 1
            try:
                os.makedirs(DOWNLOAD_DIR+dir_path)
            except:
                pass
##            print("Downloading", abs_path)
            download_file(abs_path)
downloadAndFind(URL)
print(folders, files)

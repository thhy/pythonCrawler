from urllib.parse import urlparse
from urllib import request
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import multiprocessing
queue = set()

def getWallPapperUrl(url):
    header = {}
    urls = []
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    req = request.Request(url, headers=header)
    data = request.urlopen(req)
    # print(data.read())
    #file = open('out.html','wb')
    #file.write(data.read())
    bsObj = BeautifulSoup(data, 'lxml')
    for link in bsObj.findAll('a', {"class":"preview"}):
        # print(link.attrs['href'])
        urls.append(link.attrs['href'])
    return urls

def downloadWallpaper(url, imgDir, index):
    header = {}
    header['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    req = request.Request(url, headers=header)
    data = request.urlopen(req)
    bsObj = BeautifulSoup(data, 'lxml')
    imgLink = ''
    imgFilename = ''
    filenameIdPattern = re.compile('wallhaven-(\d+)\.(jpg|png)')
    for link in bsObj.findAll('img',{'id':'wallpaper'}):
        if link.attrs['src'].startswith("//"):
            imgLink = urlparse(url).scheme+ ":" + link['src']
            print(imgLink)
            # imgFilename = re.findall(link.attrs['src'], filenameId)
            filenameId = filenameIdPattern.search(imgLink)
            if filenameId:
                print(filenameId.group())
                file = open(os.path.join(imgDir, filenameId.group()), 'wb')
                imgReq = request.Request(imgLink, header)
                try:
                    imgData = requests.get(imgLink, timeout = 20)
                    file.write(imgData.content)
                    print("download %d image success" % index)

                except BaseException:
                    print("timeout")
                    print("download %d image failed" % index)

                else:
                    pass
                time.sleep(3)

def genetateUrl(count, imgDir):
    host = 'https://alpha.wallhaven.cc/latest?'
    arg = '?page'
    index = 0
    pool = multiprocessing.Pool(processes=5)
    for i in range(count):
        arg = 'page=' + str(i)
        url = host + arg
        pages = getWallPapperUrl(url)
        for page in pages:
            print("download %d image start" %index )
            pool.apply_async(downloadWallpaper, (page, imgDir, index))
            index = index + 1
            #
            # p = multiprocessing.Process(target=downloadWallpaper, args = (page, imgDir,))
            # p.start()

def main():
    pathname = time.strftime('%Y%m%d%H%M%S', time.localtime())
    print(pathname)
    imgDir = 'D:/wallpaper'
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)
    imgDir = os.path.join(imgDir, pathname)
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)

    genetateUrl(10, imgDir)


if __name__ == '__main__':
    main()
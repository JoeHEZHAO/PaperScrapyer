 # __author__ == 'He Zhao'
 # __date__ = '03.22.2018'
 # -*- coding:utf-8 -*-

import urllib2
import re
import os, sys

class PaperScraper:
    def __init__(self, baseURL, save_dir, httpHead='http://openaccess.thecvf.com/'):
        self.baseURL = baseURL
        self.paper_link = []
        self.save_dir = save_dir
        self.httpHead = httpHead

    def getPage(self, pageNum=1):

        try:
            url = self.baseURL
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)

            return response.read()

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print("Connecting with baidu failure because {}".format(e))

    def _getPdf(self):
        page = self.getPage()
        pattern = re.compile('"content_cvpr_2017/papers/.*?>pdf</a>', re.S)
        result = re.findall(pattern, page)
        
        if result:
            self.paper_link = result
        else:
            return None

    def save_file(self):
        self._getPdf()

        for link in self.paper_link:
            fileName = link.split('/')[-2][:-6]
            filePath = os.path.join(self.save_dir, fileName)
            link = self.httpHead + link[1:-9]

            self.download_file(link, filePath)
            print("Downloaded paper {}".format(fileName))

    def download_file(self, download_url, fileName):
        response = urllib2.urlopen(download_url)
        file = open(fileName, 'wb')
        file.write(response.read())
        file.close()
        print("Completed")

if __name__ == '__main__':
    
    dest = '/home/zhufl/Dropbox/cvpr2017'
    baseURL = 'http://openaccess.thecvf.com/CVPR2017.py'
    ps = PaperScraper(baseURL, dest)
    ps.save_file()
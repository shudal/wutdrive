import os
from bs4 import BeautifulSoup
import time
import urllib3
import requests
from requests_toolbelt import MultipartEncoder
class CloudClient:
    def __init__(self, uname, passwd):
        self.uname = str(uname)
        self.passwd = str(passwd)
        self.files = []
        self.fileDict = {}
        self.proxies = {
            'http': '127.0.0.1:8888',
            'https': '127.0.0.1:8888'
        }
        self.commonHeader = {
            "Origin": 'http://jxpt.whut.edu.cn:81',
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Host': 'jxpt.whut.edu.cn:81',
        }
        self.login()
    def login(self):
        self.s = requests.Session()
        url = "http://jxpt.whut.edu.cn:81/moocresource/servlet/loginServlet?url=L21vb2NyZXNvdXJjZS9pbmRleC9pbmRleC5qc3A="
        data = {
            'username': self.uname,
            'password': self.passwd,
            'token':  str(int(time.time())*1000)
        }
        r = self.s.post(url, data=data)
    def upload(self, filePath):
        self.getFileList()
        url = "http://jxpt.whut.edu.cn:81/moocresource/resource/addResourceInfo.do"
        fileName = os.path.split(filePath)[1]
        if self.checkFileExist(fileName):
            print("文件名已存在")
            return
        fields = {
            'mySelfFolderId': "47373",
            'type': "2",
            'title': fileName,
            'file': (fileName, open(filePath, "rb")),
            'id': "",
            'fileId': "",
            'keyWord': "",
            'description': "",
            'content': "",
            'url': "",
            'oldFolderId': ""
        }
        m = MultipartEncoder(fields)
        headers =  {
            'Content-Type': m.content_type,
            'enctype': m.content_type,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate',
            'Accept': '*/*',
            "Referer": "http://jxpt.whut.edu.cn:81/moocresource/resource/addResourceInfo.do",
        }
        headers.update(self.commonHeader)
        self.s.headers.update(headers)
        r = self.s.post(url, data=m)
        print("上传成功");
    def download(self, fileName, filePath):
        self.getFileList()
        if not self.checkFileExist(fileName):
            print('文件不存在')
            return
        url = "http://jxpt.whut.edu.cn:81/moocresource/resource/downloadResourceInfo.do?resId="
        url = url + self.fileDict[fileName]
        r = self.s.get(url, stream=True)
        with open(filePath + fileName, "wb") as f:
            for c in r.iter_content(chunk_size=1024):
                if c:
                    f.write(c)
    def getFileList(self):
        url  = "http://jxpt.whut.edu.cn:81/moocresource/resource/resourceInfoList.do?mySelfFolderId="
        r = self.s.get(url,headers=self.commonHeader)
        soup = BeautifulSoup(str(r.text), 'html.parser')
        ts =  soup.select('a[href ^="/moocresource/resource/viewResourceInfo.do?id="]')
        self.files = []
        self.fileDict = {}
        for i in range(0, len(ts)):
            f = {
                'id': str(ts[i]['href'][46:]),
                'name': str(ts[i].text)
            }
            self.files.append(f)
            self.fileDict[f['name']] = f['id']
        print(self.files)
    def checkFileExist(self, fileName):
        if str(fileName) in self.fileDict:
            return True
        return False

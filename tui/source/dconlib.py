import os
import sys
import requests
import tempfile
import shutil
import zipfile 
from bs4 import BeautifulSoup
from io import BytesIO
from io import StringIO
import base64
import time


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    if iteration == total: 
        print()

def conlist(idxnum):
    condata=[]
    url = "https://dccon.dcinside.com/index/package_detail"
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"package_idx\"\r\n\r\n"+ idxnum +"\r\n-----011000010111000001101001--\r\n"
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        'origin': "https://dccon.dcinside.com",
        'referer': "https://dccon.dcinside.com/",
        'x-requested-with': "XMLHttpRequest",
        'content-type': "multipart/form-data; boundary=---011000010111000001101001"
    }
    response=requests.post(url,headers=headers,data=payload)
    json = response.json()["detail"]
    condata.append(response.json()["info"]["title"])
    for data in json:
        condata.append([data["title"],data["ext"],data["path"]])
    return condata

def getcon(no):
    headers={
        'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        ,'Referer':"https://dccon.dcinside.com/"
        ,'Sec-Fetch-Mode':"no-cors"
    }
    url='https://dcimg5.dcinside.com/dccon.php?no='+no
    return requests.get(url,headers=headers).content
    
def condown(indexnum):
    mf = BytesIO()
    condata = conlist(indexnum)
    with zipfile.ZipFile(mf, 'w', zipfile.ZIP_DEFLATED) as zipf:
        l=len(condata[1:])
        for i, con in enumerate(condata[1:]):
            imgfile= getcon(con[2])
            zipf.writestr(condata[0]+"/"+con[0]+'.'+con[1],imgfile)
            printProgressBar(i + 1, l, prefix = condata[0]+':', suffix = '완료', length = 20)
        zipf.close()
    with open(condata[0]+".zip", "wb") as f:
        f.write(mf.getvalue())

def getlist(pg,url2):
    namelist = []
    web_url = "https://dccon.dcinside.com/hot/"+str(pg)+url2
    with requests.get(web_url,headers={'referer': "https://dccon.dcinside.com"}) as response:
        #html = response.read()
        soup = BeautifulSoup(response.text, 'html.parser')
        unorder = soup.find('ul', {'class' : 'dccon_shop_list hotdccon clear'})
        lis = unorder.find_all('li')
        for ind, i in enumerate(lis):
            name = i.find('a').find('strong').text
            with requests.get(i.find('a').find('img')['src'],headers={'referer': "https://dccon.dcinside.com"}) as imgres:
                imgsrc = ("data:" + imgres.headers['Content-Type'] + ";" + "base64," + base64.b64encode(imgres.content).decode("utf-8"))
            author = i.find('a').find('span', {'class' : 'dcon_seller'}).text
            namelist.append([name,i['package_idx'],author,imgsrc,"imgc"+str(ind)])
    return namelist

def gethotlist():
    namelist = []
    web_url = "https://dccon.dcinside.com"
    with requests.get(web_url,headers={'referer': "https://dccon.dcinside.com"}) as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        unorder = soup.find('ul', {'class' : 'dccon_shop_list hotdccon clear'})
        lis = unorder.find_all('li')
        for i in lis:
            name = i.find('a').find('strong').text
            with requests.get(i.find('a').find('img')['src'],headers={'referer': "https://dccon.dcinside.com"}) as imgres:
                imgsrc = ("data:" + imgres.headers['Content-Type'] + ";" + "base64," + base64.b64encode(imgres.content).decode("utf-8"))
            author = i.find('a').find('span', {'class' : 'dcon_seller'}).text
            namelist.append([name,i['package_idx'],author,imgsrc])
    return namelist

if __name__ == '__main__':
    if len(sys.argv) == 2:
        condown(str(sys.argv[1]))
    else:
        print("You need to input dccon number!")


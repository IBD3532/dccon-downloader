import os
import sys
import requests
import tempfile
import shutil
import zipfile

def zipdir(path, ziph,name):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),name+"/"+file)

def conlist(idxnum):
    condata=[]

    url = "https://dccon.dcinside.com/index/package_detail"
    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"package_idx\"\r\n\r\n{idxnum}\r\n-----011000010111000001101001--\r\n"
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

def getcon(name,ext,no,loc):
    headers={
        'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        ,'Referer':"https://dccon.dcinside.com/"
        ,'Sec-Fetch-Mode':"no-cors"
    }
    #no='62b5df2be09d3ca567b1c5bc12d46b394aa3b1058c6e4d0ca41648b65def246ef370f2c98beb6d6b0c2baf3949e0315f109737dec282bfa41a9579994ef309264cb6444575'
    url='https://dcimg5.dcinside.com/dccon.php?no='+no
    response = requests.get(url,headers=headers)
    with open(loc+"/"+name+'.'+ ext,'wb') as f:
        f.write(response.content)

def condown(indexnum):
    condata = conlist(indexnum)
    tempdir=tempfile.mkdtemp(dir='./')
    #print("Tempdir Successfully created at : " + tempdir)
    for data in condata[1:]:
        getcon(data[0],data[1],data[2],tempdir)
    zipf = zipfile.ZipFile('./'+condata[0]+".zip", 'w', zipfile.ZIP_DEFLATED)
    zipdir(tempdir, zipf,condata[0])
    zipf.close()
    #print("Completed making ZIP File")

    shutil.rmtree(tempdir)
    #print("Successfully deleted Tempdir")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        condown(str(sys.argv[1]))
    else:
        print("You need to input dccon number!")



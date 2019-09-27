from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

url1="https://dccon.dcinside.com/hot/1/title/"
url2 = urllib.parse.quote_plus(str(input("검색어를 입력하세요.")))
web_url = url1+url2
namelist = []
idxlist = []
with urllib.request.urlopen(web_url) as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    unorder = soup.find('ul', {'class' : 'dccon_shop_list hotdccon clear'})
    lis = unorder.find_all('li')
    for i in lis:
        a = i.find('a')
        name = a.find('strong')
        namelist.append([name.text,i['package_idx']])


print(namelist)
num = int(input("번호를 입력하세요"))
finalurl = web_url + "#" + namelist[num][1]

driver = webdriver.PhantomJS('./phantomjs/bin/phantomjs.exe')
driver.get(finalurl)
unorder = driver.find_element_by_class_name('dccon_list')
lis = unorder.find_elements_by_tag_name('li')
imgname=0

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),('referer',finalurl)]
urllib.request.install_opener(opener)

for i in lis:
    sp = i.find_element_by_tag_name('span')
    img = sp.find_element_by_tag_name("img")  # 이미지 태그
    img_src = img.get_attribute('src') # 이미지 경로
    urllib.request.urlretrieve(img_src, "./img/" + str(imgname) + '.jpg')
    imgname+=1

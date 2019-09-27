from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

url1="https://dccon.dcinside.com/hot/1/title/"
url2 = urllib.parse.quote_plus(str(input("�˻�� �Է��ϼ���.")))
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

temp = 0
for i in namelist:
    print(str(temp) + "." + str(i[0]))
    temp+=1
num = int(input("��ȣ�� �Է��ϼ���: "))
finalurl = web_url + "#" + namelist[num][1]

print("\n������ ���� ��..")
options = Options()
options.binary_loction = "./chrome/ChromePortable.exe"
options.add_argument('headless')
options.add_argument("--disable-gpu")
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chrome/chromedriver.exe',options=options)

driver.get(finalurl)
unorder = driver.find_element_by_class_name('dccon_list')
lis = unorder.find_elements_by_tag_name('li')
imgname=0

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),('referer',finalurl)]
urllib.request.install_opener(opener)

print("�ٿ�ε带 �����մϴ�.")
for i in lis:
    sp = i.find_element_by_tag_name('span')
    img = sp.find_element_by_tag_name("img")  # �̹��� �±�
    img_src = img.get_attribute('src') # �̹��� ���
    urllib.request.urlretrieve(img_src, "./img/" + str(imgname) + '.jpg')
    imgname+=1
    print("���� ��(" + str(imgname) + "/" + str(len(lis)) + ")")
print("�ٿ�ε带 �Ϸ��߽��ϴ�.")
driver.quit()

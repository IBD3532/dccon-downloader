from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests

def main():
    url1="https://dccon.dcinside.com/hot/1/title/"
    url2 = urllib.parse.quote_plus(str(input("검색어를 입력하세요.")))
    web_url = url1+url2
    namelist = []
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
    num = int(input("번호를 입력하세요: "))
    finalurl = web_url + "#" + namelist[num][1]

    print("\n브라우저 실행 중..")
    options = Options()
    options.binary_loction = "./chrome/ChromePortable.exe"
    options.add_argument('headless')
    options.add_argument("--disable-gpu")
    options.add_argument('lang=ko_KR')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('./chrome/chromedriver.exe',options=options)

    driver.get(finalurl)
    unorder = driver.find_element_by_class_name('dccon_list')
    lis = unorder.find_elements_by_tag_name('li')
    imgname=0

    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'),('referer',finalurl)]
    urllib.request.install_opener(opener)

    print("다운로드를 시작합니다.")
    for i in lis:
        sp = i.find_element_by_tag_name('span')
        img = sp.find_element_by_tag_name("img")  # 이미지 태그
        img_src = img.get_attribute('src') # 이미지 경로
        urllib.request.urlretrieve(img_src, "./img/" + str(imgname) + '.jpg')
        imgname+=1
        print("저장 중(" + str(imgname) + "/" + str(len(lis)) + ")")
    print("다운로드를 완료했습니다.")
    driver.quit()

if __name__ == "__main__":
    main()
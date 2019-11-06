from bs4 import BeautifulSoup
import requests
import dconlib
from time import sleep

def getlist(pg,url2):
    namelist = []
    web_url = "https://dccon.dcinside.com/hot/"+str(pg)+url2
    with requests.get(web_url) as response:
        #html = response.read()
        soup = BeautifulSoup(response.text, 'html.parser')
        unorder = soup.find('ul', {'class' : 'dccon_shop_list hotdccon clear'})
        lis = unorder.find_all('li')
        for i in lis:
            a = i.find('a')
            name = a.find('strong')
            namelist.append([name.text,i['package_idx']])
    return namelist

def main():
    url2 = "/title/" + str(input("검색어를 입력하세요: "))
    web_url = "https://dccon.dcinside.com/hot/1"+url2
    selindex=[]
    i=1
    with requests.get(web_url) as response:
        #html = response.read()
        soup = BeautifulSoup(response.text, 'html.parser')

        if type(soup.find('div', {'class' : 'dccon_search_none'})) == type(None):
            if type(soup.find('a', {'class' : 'page_end'})) != type(None):
                endpg = soup.find('a', {'class' : 'page_end'})['href'].split("/")[4]
            else:
                if type(soup.find('div', {'class':'bottom_paging_box'}).find('a')) != type(None):
                    endpg = soup.find('div', {'class':'bottom_paging_box'}).find_all('a')[0]['href'].split("/")[4]
                else:
                    endpg = 1
        else:
            print("검색결과가 없습니다. 프로그램을 종료합니다.")
            sleep(2)
            exit()
    while True:
        try:
            print()
            dclist=getlist(i,url2)
            for idx, con in enumerate(dclist):
                print("[ {:^3} ]:".format(idx),con[0])
            print("페이지 (",i,"/",endpg,")")
            inps = str(input("번호를 입력하세요(이전:b,다음:n): ")).split()
            for inp in inps:
                if inp == 'n' or inp == 'N':
                    if i==endpg:
                        print("마지막 페이지입니다.")
                    else:
                        i+=1
                elif inp == 'b' or inp == 'B':
                    if i==1:
                        print("첫번째 페이지입니다.")
                    else:
                        i-=1
                elif int(inp) >= 0 and int(inp)<len(dclist):
                    selindex.append(dclist[int(inp)][1])
                else:
                    print("잘못 입력했습니다.")
            if len(selindex) >= 1:
                break
        except ValueError:
            print("값이 잘못됐습니다.")
    print()
    for dlist in selindex:
        dconlib.condown(dlist)
    print("\n다운로드를 완료했습니다.")
    sleep(2)
    
if __name__ == '__main__':
    main()

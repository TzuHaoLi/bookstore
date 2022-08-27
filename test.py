import requests
import bs4

url = "https://www.books.com.tw/web/sys_bbotm/books/190501/?loc=P_0001_3_001"
urls = []
try:
    htmlfile = requests.get(url)
    htmlfile.raise_for_status()
    objSoup = bs4.BeautifulSoup(htmlfile.text, "lxml")
    #print(htmlfile.text)

    objText = objSoup.find_all("h4")
    for data in range(len(objText)-9):
        urls.append(data.text)        
        print(data.text)

except Exception as err:
    print(f"failed{err}")

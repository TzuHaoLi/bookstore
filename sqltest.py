import requests
import bs4
import sqlite3
import time
flag = False #首次設True

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

def fourth_find_content(category, url):
    try:
        htmlfile = requests.get(url, headers= headers)
        htmlfile.raise_for_status()
        objSoup = bs4.BeautifulSoup(htmlfile.text, "lxml")
        #書名
        objBookname = objSoup.find("div", class_="mod type02_p002 clearfix").find("h1").text
        #價格
        objPrice = objSoup.find("strong", class_="price01").text
        
        #內容
        objTag = objSoup.find("div", class_="content")
        
        objDiv = objTag.find_all("div")
        content = ""
        for obj in objDiv:
            content += obj.text
        print(content)
        if(flag):
            conn = sqlite3.connect(category + ".db")
            sql = f"""insert into {category} values(?,?,?,?)"""
            
            data = (0, objBookname, int(objPrice), content)
            conn.execute(sql, data)
            conn.commit()
                
            conn.close()
        else:
            conn = sqlite3.connect(category + ".db")
            sql = f"""insert into {category}(name, price, content) values(?,?,?)"""
            
            data = (objBookname, int(objPrice), content)
            conn.execute(sql, data)
            conn.commit()
                
            conn.close()
        time.sleep(10)
    except Exception as err:
        print(f"failed{err}")

def third_find_book(category, url): #

    try:
        htmlfile = requests.get(url, headers=headers)
        htmlfile.raise_for_status()
        objSoup = bs4.BeautifulSoup(htmlfile.text, "lxml")
        #print(htmlfile.text)

        #objText = objSoup.find_all("h4")
        objTag = objSoup.select(".item") # id = "#XXX" , class = ".XXX"
        #objTag = objSoup.find_all("div", class_="item")
        for i in range(len(objTag)):
            objText = objTag[i].find("h4")
            #print(objText.text)
            
            obja = objText.find("a")
            fourth_find_content(category, obja.get("href"))
            if(flag):
                break
            


    except Exception as err:
        print(f"failed{err}")

def second_find_list(category, url):
    try:
        htmlfile = requests.get(url, headers=headers)
        htmlfile.raise_for_status()
        objSoup = bs4.BeautifulSoup(htmlfile.text, "lxml")
        #print(htmlfile.text)

        #objText = objSoup.find_all("h4")
        objTag = objSoup.select("body > div.container_24.main_wrap.clearfix > div.grid_4.pull_20.side_left_column > div.mod_b.type02_l001.clearfix > ul > li > ul") # id = "#XXX"
        for obj in objTag:
            objLi = obj.find_all("li")
            for objData in objLi:
                objSpan = objData.find("span")
                objA = objSpan.find("a")
                third_find_book(category, objA.get("href"))
                if(flag):
                    break
    except Exception as err:
        print(f"failed{err}")

def sqlForCategory(name):
    conn = sqlite3.connect(name + ".db")

    cursor = conn.cursor()
    sql = f"""Create table {name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price INTEGER,
                content TEXT)"""

    cursor.execute(sql)
    cursor.close()

    conn.close()

def first_find_category():
    url = "https://www.books.com.tw/web/books/?loc=menu_1_001/"
    try:
        htmlfile = requests.get(url, headers= headers)
        htmlfile.raise_for_status()
        objSoup = bs4.BeautifulSoup(htmlfile.text, "lxml")
        #print(htmlfile.text)

        #objText = objSoup.find_all("h4")
        objTag = objSoup.find("div", class_="mod_b type02_l001-1 clearfix")
        
        objTag = objTag.find("ul")
        objTag = objTag.find_all("li")

        #sqlite
        
        conn = sqlite3.connect("bookstore.db")
        if(flag):
            sql = """Create table bookstore(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category text)"""

            conn.execute(sql)
            conn.commit()
        
        for i in range(11):
            objSpan = objTag[i].find("span")
            objText = objSpan.find("a")

            if(flag):
                sql = """insert into bookstore values(?,?)"""
                data = (i, objText.text)
                conn.execute(sql, data)
                conn.commit()
                sqlForCategory(objText.text)
            second_find_list(objText.text, objText.get("href"))
        
        conn.close()
    except Exception as err:
        print(f"failed{err}")
first_find_category()

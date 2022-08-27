import sqlite3

class Menu():
    
    def __init__(self):
        self.option = []   #串列[選項字串]
        self.method = []   #串列[物件class]
    
    def display(self):     #顯示選項字串
        for i in range(len(self.option)):
            print('%d. %s' %(i+1,self.option[i]))
            
    def choose(self):      #輸入
        c = int(input('輸入選項:'))
        
        return c
    
    def handle(self, num = 1,para = False): #執行功能(class) => class.__init__
        if para :
            s = self.method[num](self.option[num])
        else :
            s = self.method[num]()
        return s

class Book_store(Menu):

    def __init__(self):
        Menu.__init__(self)
        self.option = ['書籍分類', '購物車', '會員登入', '加入會員', '離開']
        self.method = [Book_class,Cart]
    
class Book_class(Menu):
    
    def __init__(self):
        Menu.__init__(self)
        
        conn = sqlite3.connect("bookstore.db")
        sql = """SELECT * FROM bookstore"""
        result = conn.execute(sql)
        for record in result:
            self.method.append(Book_category)
            self.option.append(record[1])
        
class Book_category(Menu):
        
    def __init__(self, name):
        Menu.__init__(self)
        self.name = name
        conn = sqlite3.connect(f"{name}.db")
        sql = f"""SELECT * FROM {name}"""
        result = conn.execute(sql)
        self.book_id =[]
        for record in result:
            self.option.append(record[1])
            self.method.append(Book)
            self.book_id.append(record[0])
        #self.page = 1
    def display(self):
        if(len(self.option) < 9):
            for i in range(len(self.option)):
                print('%d.%s' %(i+1,self.option[i]))
            print('%d.離開' %(len(self.option)+2))
        else:
            for i in range(8):
                print('%d.%s' %(i+1,self.option[i]))
            print('9.下一頁\n10.離開')
    def handle(self, num = 1,para = False): #執行功能(class) => class.__init__
        s = self.method[num](self.book_id[num],self.name)
        return s
        
cart_list = []        
class Book(Menu):

    def __init__(self, id_ ,class_):
        Menu.__init__(self)
        
        conn = sqlite3.connect(f"{class_}.db")
        sql = f"""SELECT * FROM {class_}
                WHERE id = {id_}"""
        result = conn.execute(sql)
        for record in result:
            self.name = record[1]
            self.price = record[2]
            self.content = record[3]
        
        self.option = ['加入購物車', '回上一步']
        self.method = [self.Add_to_cart]
        
    def display(self):
        print('書名:', self.name)
        print('價錢:', self.price)
        print('內容:', self.content)
        
        Menu.display(self)

    def handle(self, num, para):
        s = self.method[num](self.name)
        return s

    def Add_to_cart(self, name):
        cart_list.append(name)
        print('成功加入購物車')
        return Book_store()
        


class Cart(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.option = ['回主選單']
        self.method = [Book_store]
        5
    def display(self):
        for i in range(len(cart_list)):
            print(' %s' %(cart_list[i]))
        Menu.display(self)

class Member(Menu):

    def __init__(self):
        self.accountID = ''
        self.passwd = ''
        self.mail = ''
        
class Sign_in(Member):
    
    def __init__(self):
        Member.__init__(self)
        
    
member_data = [] #class member
'''class Register(Member):
    def __init__(self):
        Member.__init__(self)
        Menu.__init__()
    def register(self):
        print('如果要取消註冊請輸入[取消]')
        
        print('請輸入帳號:',)
        a = input()
        if self.accountID == '取消'     
        else 
            self.accountID = a
            print('請輸入密碼:')
            if self.passwd == '取消'
        self.passwd = input()
        print('請輸入電子信箱:')
        self.mail = input()
    def cancle(self):
'''     

        
para = {Book_store:False, Book_class:True, Book_category:True, Book:True,Cart:False}

t = Book_store()



while(True):
    p = t.__class__
    print(p)
    t.display()

    
    while(True):    #輸入判斷
        s = t.choose()
        if s in range(len(t.option)+1):
            break
        else:
            print('錯誤,請重新輸入')
        
    t = t.handle(s-1,para[p])
        
               
    
            


    

    

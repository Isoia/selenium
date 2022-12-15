import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager

searchword = ""
page = 0
excelname = ""
review = ""
buy_num = ""


root = tk.Tk()
root.title('검색창')
root.geometry("350x200+100+100")

lb1 = tk.Label(root,text="검색어",width=5,height=1,font=('맑은 고딕',13,'bold'),fg='black')
lb1.grid(row=0,column=0,padx=5,pady=10)

lb2 = tk.Label(root,text="검색 페이지수",width=10,height=1,font=('맑은 고딕',13,'bold'),fg='black')
lb2.grid(row=1,column=0,padx=5,pady=10)

lb3 = tk.Label(root,text="엑셀이름",width=10,height=1,font=('맑은 고딕',13,'bold'),fg='black')
lb3.grid(row=2,column=0,padx=5,pady=10)

input1 = tk.Entry(font=('맑은고딕',13),width=20)
input1.grid(row=0,column=1,padx=5,pady=10)

input2 = tk.Entry(font=('맑은고딕',13),width=5)
input2.place(x=120,y=62)

input3 = tk.Entry(font=('맑은고딕',13),width=20)
input3.place(x=120,y=112)

def btnclick():
    searchwordbefore = input1.get()
    searchword = searchwordbefore.replace(' ','%20',searchwordbefore.count(' '))
    page = int(input2.get())
    excelname = input3.get()

    f = open(rf"C:\Users\진진\Desktop\{excelname}.csv", 'w', encoding='CP949', newline='')
    csvWriter = csv.writer(f)
    csvWriter.writerow(["이름", "가격", "리뷰 개수", "구매 링크"])   

    for pages in range(1,page+1):
        service = Service(executable_path=ChromeDriverManager().install())
        browser = webdriver.Chrome(service = service)
        browser.get(f'https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery={searchword}&pagingIndex={pages}&pagingSize=40&productSet=total&query={searchword}&sort=rel&timestamp=&viewType=list')
        browser.implicitly_wait(5)

        before_h = browser.execute_script("return window.scrollY")

        while(True):
            browser.find_element_by_css_selector("body").send_keys(Keys.END)

            time.sleep(1)

            after_h = browser.execute_script("return window.scrollY")

            if after_h == before_h:
                break
            before_h = after_h 



        items = browser.find_elements_by_css_selector(".basicList_info_area__17Xyo") 

        for item in items:
            name = item.find_element_by_css_selector(".basicList_title__3P9Q7").text
            try:
                price = item.find_element_by_css_selector(".price_num__2WUXn").text
            except:
                price = "판매중단"
            link = item.find_element_by_css_selector(".basicList_title__3P9Q7 > a").get_attribute('href')
            try:
                review = item.find_elements_by_css_selector('.basicList_num__1yXM9')[0].text
            except:
                review = "리뷰 없음"
           
            print(name,price,review)
            #데이터 쓰기
            csvWriter.writerow([name, price, review, link])           
    

btn1 = tk.Button(root,text='검색',font=('맑은 고딕',10,'bold'),fg='black',width=4,command=btnclick)
btn1.place(x=150,y=150)

root.mainloop()

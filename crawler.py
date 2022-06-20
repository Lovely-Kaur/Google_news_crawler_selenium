from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


word = input("Enter the search keyword")
url = "https://news.google.com/"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver.maximize_window()
driver.get(url)


driver.find_element(By.XPATH, '//input[@class="Ax4B8 ZAGvjd"]').send_keys(word)
driver.find_element(By.XPATH, '//button[@class="gb_lf"]').click()

driver.implicitly_wait(30)

try:
    startdate = input("Enter starting date in YYYYMMDD format")
    enddate = input("Enter ending date in YYYYMMDD format")
    y1 = int(startdate[0:4])
    m1 = int(startdate[4:6])
    d1 = int(startdate[6:])
    y2 = int(enddate[0:4])
    m2 = int(enddate[4:6])
    d2 = int(enddate[6:])


    articledivs = driver.find_elements(By.XPATH,'//div[@class="xrnccd"]')
    articledivs1 = driver.find_elements(By.XPATH,'//div[@class="SVJrMe"]')
    newslist=[]

    for articlediv in articledivs:
        try:
            title = articlediv.find_element(By.TAG_NAME,"h3").text
            date = articlediv.find_element(By.TAG_NAME,"time").get_attribute("datetime")[0:10]
            link = articlediv.find_element(By.TAG_NAME,"a").get_attribute("href")
            publisher = articlediv.text[(articlediv.text).index("\n")+1:(articlediv.text).index("\n",(articlediv.text).index("\n")+1)]
            newsarticle = {
                # 'data' : articlediv.text
                'title' : title,
                'publisher' : publisher,
                'link' : link,
                'date' : date
            }
            y3 = int(newsarticle["date"][0:4])
            m3 = int(newsarticle["date"][5:7])
            d3 = int(newsarticle["date"][8:10])
            if(y1==y2):
                if (m1==m2):
                    if (d3>=d1 and d3<=d2):
                        newslist.append(newsarticle)
                else:
                    if (m3==m1):
                        if(d3>=d1):
                            newslist.append(newsarticle)
                    elif (m3==m2):
                        if(d3<=d2):
                            newslist.append(newsarticle)
                    else:
                        newslist.append(newsarticle)
            elif(y3>=y1 and y3<=y2):
                if (y3==y1):
                    if(m3>=m1):
                        newslist.append(newsarticle)
                elif(y3==y2):
                    if(m3<=m2):
                        newslist.append(newsarticle)
                else:
                    newslist.append(newsarticle)
        except:
            pass

       
except:
    pass

df = pd.DataFrame(newslist)
df.to_csv('News.csv')
print('Saved to CSV File.')
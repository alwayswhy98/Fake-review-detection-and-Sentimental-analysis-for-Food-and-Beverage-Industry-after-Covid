import pandas as pd
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import numpy as np


class naver_review():
    def __init__(self):
        option = Options()
        option.binary_location="C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

        df = pd.read_csv("naver_url.csv")
        urls = df["URL"]
        file_cnt = 1
        for url in urls[:1]:
            self.scrap_reviews(option, url, file_cnt)
            file_cnt += 1

    def scrap_reviews(self, option, url, file_cnt):
        brower = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=option)

        ratings = []
        dates = []
        titles = []
        contents = []
        helpfuls = []

        brower.get(url)
        time.sleep(2)
        #Move to Reviews
        review_btn = brower.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[3]/ul/li[2]/a')
        review_btn.click()



        page_cnt = 1
        flag = True

        #Gather reviews
        while flag:
            reviews = brower.find_elements(By.CLASS_NAME,"_2389dRohZq")
            print("len reviews: ", len(reviews))
            for review in reviews:
                #print(review)
                html_code = review.get_attribute("innerHTML")
                html_code = html_code.replace("\n", " ")
                #print(html_code)
                rating_result = re.search('(.*)<em class="_15NU42F3kT">(.*)</em>(.*)', html_code)
                if rating_result:
                    rating = rating_result.group(2)
                    ratings.append(rating)
                else:
                    ratings.append(np.nan)
                    #print(rating)
                date_result = re.search('(.*)</strong><span class="_3QDEeS6NLn">(.*)</span><div class="_1JZCQjfNPR">(.*)', html_code)
                if date_result:
                    date = date_result.group(2)
                    dates.append(date[:8])
                else:
                    dates.append(np.nan)
                    #print(date)
                title_result = re.search('(.*)<button class="_3jZQShkMWY" aria-expanded="false" disabled=""><span class="_3QDEeS6NLn">(.*)</span></button></div></div></div></div><div class="_19SE1Dnqkf">(.*)', html_code)
                if title_result:
                    title = title_result.group(2)
                    title = title.replace("\n", " ")
                    titles.append(title)
                else:
                    titles.append(np.nan)
                    #print(title)
                content_result = re.search('(.*)<div class="YEtwtZFLDz"><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="Ogt5tXwmlq">(.*)', html_code)
                if content_result:
                    content = content_result.group(2)
                    content = content.replace("\n", " ")
                    contents.append(content)
                else:
                    content_result = re.search('(.*)<div class="YEtwtZFLDz vlXMQEAtPR"><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="Ogt5tXwmlq">(.*)', html_code)
                    if content_result:
                        content = content_result.group(2)
                        content = content.replace("\n", " ")
                        contents.append(content)
                    else:
                        content_result = re.search('(.*)</span><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="Ogt5tXwmlq">(.*)', html_code)
                        if content_result:
                            content = content_result.group(2)
                            content = content.replace("\n", " ")
                            contents.append(content)
                        else:
                            content_result = re.search('(.*)</span><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="_2QRtghbCyu">(.*)', html_code)
                            if content_result:
                                content = content_result.group(2)
                                content = content.replace("\n", " ")
                                contents.append(content)
                            else:
                                content_result = re.search('(.*)</span><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="fgI31XFKxN">(.*)', html_code)
                                if content_result:
                                    content = content_result.group(2)
                                    content = content.replace("\n", " ")
                                    contents.append(content)
                                else:
                                    content_result = re.search('(.*)<div class="YEtwtZFLDz"><span class="_3QDEeS6NLn">(.*)</span></div>(.*)<div class="fgI31XFKxN">(.*)', html_code)
                                    if content_result:
                                        content = content_result.group(2)
                                        content = content.replace("\n", " ")
                                        contents.append(content)
                                    else:    
                                        contents.append(np.nan)
                    #print(content)
                helpful_result = re.search('(.*)<span class="count">(.*)</span></button>(.*)', html_code)
                if helpful_result:
                    helpful = helpful_result.group(2)
                    helpfuls.append(helpful[0])
                else:
                    helpfuls.append(np.nan)
                    #print(helpful)

                time.sleep(2)

            page_cnt += 1
            print(page_cnt)
            if page_cnt % 10 != 1:
                page_num = page_cnt%10 + 1
                if page_num != 1:
                    page_btn = brower.find_element(By.XPATH, f'//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[{page_num}]')
                else:
                    page_btn = brower.find_element(By.XPATH, f'//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[11]')
                    
                try:
                    page_btn.click()
                except:
                    flag = False
                    print("end page")

            else:
                page_btn = brower.find_element(By.XPATH, '//*[@id="REVIEW"]/div/div[3]/div/div[2]/div/div/a[12]')
                page_btn.click()

            time.sleep(3)

        data = {
            "rating": ratings,
            "date": dates,
            "helpful count": helpfuls,
            "title": titles,
            "content": contents
        }

        df = pd.DataFrame(data)
        filename = str(file_cnt) + ".csv"
        df.to_csv(filename, encoding='utf_8_sig')



naver  = naver_review()


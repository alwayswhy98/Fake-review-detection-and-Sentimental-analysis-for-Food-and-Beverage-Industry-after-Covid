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


class naver_review():
    def __init__(self):
        option = Options()
        option.binary_location="C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
        
        #Open URL
        url = "https://adcr.naver.com/adcr?x=rbGr6A9tDKfgmzmZEurPsP///w==kKjnm+pMyYcQ+CpuX2lDsDBxNDLBP8G5dsSMVKmg2XwWdb1VgVF9aEJIwIOIptUEmlwKG7zRJwCR/mI0ciN5mO4cpliVk8lisRZbCtuYe+Oh+ymjISMEjj7hkVxru6nd2NMtg3o/uPJ490GDC8C2LLbsyaNn31d/eZBmVpINCsm2JXGBogS3cTSYd5L9HhP0ipkTszx2NTEqCdbN0CVtcFfoqKmvxRxyEHZmKl5UV7Kr9iEPzIYeBbK1wZe0l7MDV3Ef7FhwSAwW9I0ZkmB/cUSgWJL1kn8zIL8pcU6WvgIALyAIlgRD4eAIiy9/fBjOWS1SJ1UxwdiyHXw84m5Or1r3byIdAYOz6uO8G5MFSa8XDajog0kKX67IQLKa2FJNLFos/G5THkcen8lR9S7wo0AsJFxVcv/kZkQFVeAZUYZoS4KCJ/BVNtG6sxgFssb6invo/+UB44sKZ21vtkATfJn41JW4XG5pV8YW0ZX+Ey+ivluWxFXElalFM+A2eekE0iNVL+AcvDLgPXo/dYATreZAyDbPc98+lD1JuAgnthTE9TL4oQm7SBfVYF7DiqIV1gdApm5ipJ7Ggx9xVpUYvrnSvIIrAwz4iesd+N7PxeBOPQcO5p+h0JNXkwdCat6O5s4dHa7A+ylOOc5xG5hT2+/Zb5g9H2C2L65TLWZcI+eG6aSsacMukq+EqVuVBmdYpNZ9wR7pRZCvRaYScdO7GhgHYXKHUVxQwzYwfxsFAr6uYClqtQjtBIdzqe9Jdbk5eAu4UQOml8bNiSBWv141kqxa7mVWjPeyna5yUHacIp7bCzjx8gD67gv/KNFXTsG/2ovOjEAHJY5I4Yf7Rt6/Zug=="
        self.open_page(url, option)

    def open_page(self, url, option):
        brower = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=option)
        brower.get(url)
        time.sleep(2)
        #Move to Reviews
        review_btn = brower.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div[3]/ul/li[2]/a')
        review_btn.click()

        #Gather reviews
        reviews = brower.find_element(By.CLASS_NAME,"_2389dRohZq")
        #for review in reviews:
        #    print(review)
        html_code = reviews.get_attribute("innerHTML")
        html_code = html_code.replace("\n", " ")
        #print(html_code)
        rating_result = re.search('(.*)<em class="_15NU42F3kT">(.*)</em>(.*)', html_code)
        rating = rating_result.group(2)
        print(rating)
        date_result = re.search('(.*)</strong><span class="_3QDEeS6NLn">(.*)</span><div class="_1JZCQjfNPR">(.*)', html_code)
        date = date_result.group(2)
        print(date)
        title_result = re.search('(.*)<button class="_3jZQShkMWY" aria-expanded="false" disabled=""><span class="_3QDEeS6NLn">(.*)</span></button></div></div></div></div><div class="_19SE1Dnqkf">(.*)', html_code)
        title = title_result.group(2)
        print(title)
        content_result = re.search('(.*)</span></button></div></div></div></div><div class="_19SE1Dnqkf"><div class="YEtwtZFLDz vlXMQEAtPR"><span class="_3QDEeS6NLn">(.*)</span></div><span class="_2QRtghbCyu">(.*)', html_code)
        content = content_result.group(2)
        print(content)
        helpful_result = re.search('(.*)<span class="count">(.*)</span></button>(.*)', html_code)
        helpful = helpful_result.group(2)
        print(helpful)

        time.sleep(30)


naver  = naver_review()


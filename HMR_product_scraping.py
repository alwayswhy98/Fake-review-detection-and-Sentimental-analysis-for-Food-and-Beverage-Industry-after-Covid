import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def save_naver_shopping_products():
    brower = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=option)
    ad_urls = []
    product_urls = []
    non_ad_product = []

    for i in range(1, 51):
        brower.get(f"https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery=%EB%B0%80%ED%82%A4%ED%8A%B8&pagingIndex={i}&pagingSize=20&productSet=total&query=%EB%B0%80%ED%82%A4%ED%8A%B8&sort=rel&timestamp=&viewType=list")
        brower.execute_script("window.scrollTo(0, 10000);")
        time.sleep(3)
        #Extract URL of advertising products
        ad_elements = brower.find_elements(By.CLASS_NAME,"ad")
        for elem in ad_elements:
            ad_urls.append(elem.get_attribute("href"))
        #Extract URL of products
        products_elements = brower.find_elements(By.CLASS_NAME,"basicList_link__1MaTN")
        for elem in products_elements:
            product_urls.append(elem.get_attribute("href"))
        time.sleep(2)

    for product in product_urls:
        if product not in ad_urls:
            non_ad_product.append(product)
    print(len(ad_urls))
    print(len(product_urls))
    print(len(non_ad_product))

    df = pd.DataFrame(non_ad_product, columns=["URL"])
    df.to_csv("naver_url.csv")

def coupang_last_page():
    brower = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=option)
    url = "https://www.coupang.com/np/search?q=%EB%B0%80%ED%82%A4%ED%8A%B8&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=60&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1"
    brower.get(url)
    time.sleep(2)
    last_btn = brower.find_element(By.CLASS_NAME,"btn-last")
    
    return last_btn.text

def save_coupang_products():
    product_urls = []
    best_product_urls = []
    banner_product_urls = []
    final_products_urls = []
    last_page = int(coupang_last_page())
    print(last_page)

    for i in range(1, last_page+1):
        print(i)
        brower = webdriver.Chrome(service=Service(ChromeDriverManager(version='104.0.5112.20').install()), options=option)
        brower.get(f"https://www.coupang.com/np/search?q=%EB%B0%80%ED%82%A4%ED%8A%B8&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=60&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={i}")
        time.sleep(2)

        best_seller_elements = brower.find_elements(By.CLASS_NAME,"best-seller-carousel-item")
        for elem in best_seller_elements:
            pr = elem.find_element(By.CLASS_NAME,"search-product-link")
            best_product_urls.append(pr.get_attribute("href"))

        products_elements = brower.find_elements(By.CLASS_NAME,"search-product")
        for elem in products_elements:
            if "AD" in elem.text:
                pass
            else:
                pr = elem.find_element(By.CLASS_NAME,"search-product-link")
                product_urls.append(pr.get_attribute("href"))
        brower.close()
        time.sleep(5)

    for url in product_urls:
        if url not in best_product_urls:
            final_products_urls.append(url)

    print(len(final_products_urls))

    df = pd.DataFrame(final_products_urls, columns=["URL"])
    df.to_csv("coupang_url.csv")

option = Options()
option.binary_location="C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
save_naver_shopping_products()
#save_coupang_products()

def insta_post_crawling(ID, PW, page, counts):
    import os
    import shutil
    import pandas as pd
    import numpy as np
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    import requests
    from collections import Counter
    from wordcloud import WordCloud
    import time
    from datetime import datetime, timedelta
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import nltk
    import pandas as pd
    from konlpy.tag import Okt
    
    driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')  # 전체화면
    #chrome_options.add_argument('--headless')  # 브라우저 창을 열지 않고 실행하는 옵션입니다. 크롤링 과정 확인 위해 설정X
    #chrome_options.add_argument('--no-sandbox')  # 코랩 환경에서의 필수 옵션입니다.
    chrome_options.add_argument('--disable-dev-shm-usage')  # 코랩 환경에서의 필수 옵션입니다.
    chrome_options.add_argument("disable-gpu")  # 가속 사용 x 사람처럼 보이지 않으면 차단됨.
    chrome_options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.instagram.com/'
    driver.get(url)
    
    
    #배민 ID 및 PW 입력
    id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#loginForm > div > div:nth-child(1) > div > label > input')
    ))
    id_input.send_keys(ID)
    driver.implicitly_wait(10)
    
    pw_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#loginForm > div > div:nth-child(2) > div > label > input')
    ))
    pw_input.send_keys(PW)
    driver.implicitly_wait(10)
    
    #로그인
    driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(3) > button').click()
    driver.implicitly_wait(10)
    
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div').click()
    driver.implicitly_wait(10)
    
    driver.get('https://www.instagram.com/' + page + '/')
    driver.implicitly_wait(10)
    
    post_texts = []
    
    driver.find_element(By.CLASS_NAME, '_aagw').click()
    k = driver.find_element(By.CLASS_NAME, '_a9zr')
    post_texts.append(k.text)
    
    for _ in range(0, counts - 1):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
        time.sleep(1)
        k = driver.find_element(By.CLASS_NAME, '_a9zr')
        post_texts.append(k.text)

    return post_texts
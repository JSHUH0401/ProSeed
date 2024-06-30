def googleplay_review_wordcloud(url, banned):
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

    #구글플레이 접속 후 리뷰 크롤링
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    #5점짜리 리뷰만 크롤링
    allreview_button_selector = '/html/body/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/div/div[2]/div[5]/div/div/button/span'
    allreview_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, allreview_button_selector))
    )
    allreview_button.click()
    
    star_selector = '/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[2]/i'
    star_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, star_selector))
    )
    star_button.click()
    
    star5_selector = '/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[6]/div[2]/div[2]'
    star5_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, star5_selector))
    )
    star5_button.click()
    start_time = time.time()
    while time.time() - start_time < 600:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1)
    texts = []
    k = driver.find_elements(By.CLASS_NAME,'h3YV2d')
    
    #texts 리스트에 리뷰들 추출
    for i in k:
        texts.append(i.text)

    #리뷰 형태소 단위 슬라이싱
    content_text = ' '
    for each in texts:
        content_text = content_text + each + '\n'
    okt = Okt()
    noun = okt.nouns(content_text)
    
    #불용어 설정 및 최다빈도 단어 100개 추출
    stop = banned
    for i, v in enumerate(noun): #1글자 단어 제외
        if len(v)<2:
            noun.pop(i)
        elif v in stop:
            noun.pop(i)
    count = Counter(noun)
    noun_list = count.most_common(100)

    #워드클라우드 생성
    wc = WordCloud(font_path='\Library\Fonts\malgun.ttf',relative_scaling = 0.2, background_color= 'white')
    wc.generate_from_frequencies(dict(noun_list))
    wc.to_file('wordcloud.png')

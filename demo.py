from selenium import webdriver
from selenium.webdriver.common.by import By
import time

CHROMEDRIVER_PATH = 'D:/chromedriver-win64/chromedriver.exe'
options = webdriver.ChromeOptions() 
driver = webdriver.Chrome(options=options)





























'''
driver.get('https://indianexpress.com/')
href=driver.find_element(By.XPATH,'/html/body/main/div[6]/div/div[1]/div/div/div[2]/h1/a').get_attribute('href')
driver.get(href)
time.sleep(2)
headline_text = driver.find_element(By.XPATH,'/html/body/main/div[6]/div/div[1]/div/h1').text
print(headline_text)
'''

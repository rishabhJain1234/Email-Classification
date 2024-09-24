from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import csv
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException

load_dotenv()

def login_gmail(driver, email, password):
    """Log in to Gmail using the provided credentials."""
    driver.get('https://mail.google.com/')
    
    # Enter email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    )
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)
    
    time.sleep(5)
    
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search mail"]'))
    )
    
login_gmail(driver, os.getenv('GMAIL_USERNAME'), os.getenv('GMAIL_PASSWORD'))
time.sleep(5)  # Wait for inbox to load
emails = driver.find_elements("class name", "zA")
for email in emails:
    print(email.text)
driver.quit()
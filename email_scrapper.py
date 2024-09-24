import os
import time
import csv
import regex as re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementClickInterceptedException, 
    ElementNotInteractableException, 
    StaleElementReferenceException
)

# Load environment variables
load_dotenv()

# Define paths and credentials
CHROMEDRIVER_PATH = 'D:/chromedriver-win64/chromedriver.exe'
GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

def login_gmail(driver, email, password):
    """Log in to Gmail using the provided credentials."""
    driver.get('https://mail.google.com/')
    
    # Enter email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    )
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Necessary sleep due to potential Gmail load time

    # Enter password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search mail"]'))
    )

def get_latest_emails(driver, num_emails=10):
    """Scrape the latest emails from Gmail inbox."""
    email_data = []

    try:
        # Wait for the inbox to load
        inbox_locator = (By.CSS_SELECTOR, "table.F.cf.zt")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(inbox_locator)
        )

        # Find all email rows
        emails = driver.find_elements(By.CSS_SELECTOR, 'tr.zA')

        # Loop through emails and extract information
        for index in range(min(num_emails, len(emails))):
            time.sleep(1)
            try:
                email = emails[index]
                content = re.sub(r'\n', ' ', email.text)  # Clean up content

                email_link = email.find_element(By.CSS_SELECTOR, 'span.bog')
                driver.execute_script("arguments[0].click();", email_link)  # Use JS click to avoid issues

                # Wait for the email content to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.adn'))
                )

                # Extract email details
                subject = driver.find_element(By.CSS_SELECTOR, 'h2.hP').text
                sender = driver.find_element(By.CSS_SELECTOR, 'span.gD').text
                link = driver.current_url

                email_data.append({
                    'subject': subject, 
                    'sender': sender, 
                    'content': content, 
                    'link': link
                })

                print(f"Email {index + 1}: Subject: {subject}, Sender: {sender}, Content: {content[:100]}...")

                driver.back()  # Go back to the inbox

                # Re-fetch the emails to avoid stale element references
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(inbox_locator)
                )
                emails = driver.find_elements(By.CSS_SELECTOR, 'tr.zA')

            except (ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException) as e:
                print(f"Error processing email {index + 1}: {str(e)}")
                continue

    except Exception as e:
        print(f"An error occurred while retrieving emails: {e}")

    return email_data

def main():
    # Set up Chrome driver
    options = webdriver.ChromeOptions() 
    driver = webdriver.Chrome(options=options)

    try:
        # Log in to Gmail
        login_gmail(driver, GMAIL_USERNAME, GMAIL_PASSWORD)

        # Scrape the latest emails
        emails = get_latest_emails(driver, num_emails=60)

        # Save the emails to a CSV file
        csv_file = 'emails_new.csv'
        with open(csv_file, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Sender', 'Subject', 'Content', 'Link'])  # Write header
            for email in emails:
                writer.writerow([email['sender'], email['subject'], email['content'], email['link']])

        print(f"Emails saved to {csv_file}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

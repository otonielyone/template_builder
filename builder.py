import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import urllib.request
import time
import csv
import re
import sys
import os, shutil


async def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver

async def login(driver, timeout, add_username, add_password):
    driver.get("https://www.websiteeditor.realtor/home/site/94fbcdbc/rentals")
    
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_username"]')))
    add_email = driver.find_element(By.XPATH, '//input[@name="j_username"]')
    add_email.send_keys(add_username)
    
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_password"]')))
    add_pass = driver.find_element(By.XPATH, '//input[@name="j_password"]')
    add_pass.send_keys(add_password)
    
    await asyncio.sleep(3)  # Adjust as needed
    
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-auto="login-button"]')))
    login_button = driver.find_element(By.XPATH, '//button[@data-auto="login-button"]')
    driver.execute_script('arguments[0].click();', login_button)
    
async def pages_section(driver, timeout):
    #click widget section
    txt = '//label[text()="Pages"]'
    pages_section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, txt)))
    pages_section.click()

   
async def click_popups_section(driver,timeout):   
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//span[text()="Popups"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    click_popups_section = driver.find_element(by=By.XPATH, value='//span[text()="Popups"]')
    click_popups_section.click()

async def find_template_settings(driver, timeout, template):
    
    try:
        # Wait until the label element is visible
        label_element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH,  f'//label[text()="{template}"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)

        # Find the following sibling element
        next_sibling = label_element.find_element(By.XPATH, './following-sibling::*[1]')
        
        # Scroll into view if needed
        driver.execute_script("arguments[0].scrollIntoView(true);", next_sibling)
        
        # Click on the next sibling element
        next_sibling.click()
        
    except Exception as e:
        print(f"Error occurred: {e}")



async def duplicate_entry(driver, timeout, mls):
                
        await find_template_settings(driver,timeout, "Template Listing")

        # Find the "Duplicate" menu item within the context menu
        txt = "div[data-auto='duplicate'] span"
        duplicate_menu_item = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, txt))
        )

        # Scroll into view of the "Duplicate" menu item
        driver.execute_script("arguments[0].scrollIntoView(true);", duplicate_menu_item)

        # Click on the "Duplicate" menu item
        duplicate_menu_item.click()


        new_label_text = f"TT: {mls[0]}"

        # Locate the input element and clear existing value
        input_element_xpath = f"//input[@value='Copy of Template Listing']"
        input_element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, input_element_xpath))
        )
        input_element.clear()
        input_element.send_keys(new_label_text)
#        new_label_text = f"TT: {mls[0]}"
#
#        # Locate the input element based on its attributes
#        input_element = driver.find_element(By.XPATH, f"//input[@value='Copy of Template Listing']")
#        input_element.clear()  
#        input_element.send_keys(new_label_text)

        duplicate_me = driver.find_element(By.XPATH, '//div[@role="button"]')
        duplicate_me.click()


#def rename_entry(driver, timeout, mls, rename_template):
#
#        find_template = f"TT: {mls}"
#
#        find_template_settings(driver,timeout, f"{find_template}")
#
#        # Find the "Rename" menu item within the context menu
#        rename_menu_item = driver.find_element(By.XPATH, ".//div[@data-auto='rename']")
#
#        # Scroll into view of the "Rename" menu item
#        driver.execute_script("arguments[0].scrollIntoView(true);", rename_menu_item)
#
#        # Click on the "Rename" menu item
#        rename_menu_item.click()
#        
#        # Locate the input element based on its attributes
#        input_element = driver.find_element(By.XPATH, f"//input[@value='{find_template}']")
#        input_element.clear()  
#        input_element.send_keys(rename_template)
#
#        duplicate_me = driver.find_element(By.XPATH, '//div[@role="button"]')
#        duplicate_me.click()


#def delete_entry(driver, timeout, mls):
#        
#        find_template = f"TT: {mls}"
#
#        find_template_settings(driver,timeout, f"{find_template}")
#
#        # Find the "Delete" menu item within the context menu
#        delete_menu_item = driver.find_element(By.XPATH, ".//div[@data-auto='delete']")
#
#        # Scroll into view of the "Delete" menu item
#        if delete_menu_item:
#            driver.execute_script("arguments[0].scrollIntoView(true);", delete_menu_item)
#
#            # Click on the "Delete" menu item
#            delete_menu_item.click()
#
#            yes_button = driver.find_element(By.XPATH, '//button[@data-auto="yes-button"]')
#            yes_button.click()
#
#
async def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = await setup_driver()
    await login(driver, timeout, add_username, add_password)

    await pages_section(driver,timeout)
    await click_popups_section(driver,timeout)
    mls_list = ("VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456","$2000"), ("VAR7654321", "2321 Yalc Ave #1B, Bronx NY 65501", "$0002"), ("VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456","$2000"), ("VAR7654321", "2321 Yalc Ave #1B, Bronx NY 65501", "$0002")
    for mls in mls_list:
        await duplicate_entry(driver,timeout, mls)
    await asyncio.sleep(10)
    driver.quit()

if __name__ == "__main__":
    asyncio.run(main())

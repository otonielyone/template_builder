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



def setup_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver


def login(driver, timeout, add_username, add_password):
    #Go to page - will redirect to login
    driver.get("https://www.websiteeditor.realtor/home/site/94fbcdbc/rentals")

    #Find username
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//input[@name="j_username"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    add_email = driver.find_element(by=By.XPATH, value='//input[@name="j_username"]')
    add_email.send_keys(add_username)
    

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//input[@name="j_password"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    add_pass = driver.find_element(by=By.XPATH, value='//input[@name="j_password"]')
    add_pass.send_keys(add_password)


    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//button[text()="Login"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    login = driver.find_element(by=By.XPATH, value='//button[text()="Login"]')
    login.click()

def click_page_section(driver,timeout):   
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//label[text()="Pages"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    click_pages = driver.find_element(by=By.XPATH, value='//label[text()="Pages"]')
    click_pages.click()
   
def click_popups_section(driver,timeout):   
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//span[text()="Popups"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    click_popups_section = driver.find_element(by=By.XPATH, value='//span[text()="Popups"]')
    click_popups_section.click()

#def find_template_settings(driver, timeout):
#    try:
#        element_present = EC.presence_of_element_located((By.XPATH, '//label[text()="Template Listing"]'))
#        WebDriverWait(driver, timeout).until(element_present)
#
#    except TimeoutException:
#        print("Timed out waiting for Template Listing to Load")
#        sys.exit()
#
#    click_template_section = driver.find_element(by=By.XPATH, value='//label[text()="Template Listing"]')
#
#    # Find the parent div using ancestor::div with specific classes
#    parent_div = click_template_section.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ListItem-listItem') and contains(@class, 'ListItem-selectable')]")
#
#    # Scroll the SVG element into view
#    driver.execute_script("arguments[0].scrollIntoView(true);", parent_div)
#
#    # Click on the SVG icon
#    svg_icon = parent_div.find_elements(By.XPATH, '//div//span//span[@data-name="icon-settings"]')
#    svg_icon[16].click()

def find_template_settings(driver, timeout, template):

    # Wait for the label "Template Listing" to be present
    element_present = EC.presence_of_element_located((By.XPATH, f'//label[text()="{template}"]'))
    WebDriverWait(driver, 20).until(element_present)

    # Find the label element
    label_element = driver.find_element(By.XPATH, f'//label[text()="{template}"]')

    # Find the adjacent span element with data-name="icon-settings"
    adjacent_icon_settings = label_element.find_element(By.XPATH, './following::span[@data-name="icon-settings"][1]')

    # Scroll the adjacent icon settings element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", adjacent_icon_settings)

    # Perform actions on the adjacent icon settings element (e.g., click)
    adjacent_icon_settings.click()



def duplicate_entry(driver, timeout, mls):
                
        find_template_settings(driver,timeout, "Template Listing")

        # Find the "Duplicate" menu item within the context menu
        duplicate_menu_item = driver.find_element(By.XPATH, ".//div[@data-auto='duplicate']")

        # Scroll into view of the "Duplicate" menu item
        driver.execute_script("arguments[0].scrollIntoView(true);", duplicate_menu_item)

        # Click on the "Duplicate" menu item
        duplicate_menu_item.click()

        new_label_text = f"TT: {mls}"

        # Locate the input element based on its attributes
        input_element = driver.find_element(By.XPATH, f"//input[@value='Copy of Template Listing']")
        input_element.clear()  
        input_element.send_keys(new_label_text)

        duplicate_me = driver.find_element(By.XPATH, '//div[@role="button"]')
        duplicate_me.click()


def rename_entry(driver, timeout, mls, rename_template):

        find_template = f"TT: {mls}"

        find_template_settings(driver,timeout, f"{find_template}")

        # Find the "Rename" menu item within the context menu
        rename_menu_item = driver.find_element(By.XPATH, ".//div[@data-auto='rename']")

        # Scroll into view of the "Rename" menu item
        driver.execute_script("arguments[0].scrollIntoView(true);", rename_menu_item)

        # Click on the "Rename" menu item
        rename_menu_item.click()
        
        # Locate the input element based on its attributes
        input_element = driver.find_element(By.XPATH, f"//input[@value='{find_template}']")
        input_element.clear()  
        input_element.send_keys(rename_template)

        duplicate_me = driver.find_element(By.XPATH, '//div[@role="button"]')
        duplicate_me.click()


def delete_entry(driver, timeout, mls):
        
        find_template = f"TT: {mls}"

        find_template_settings(driver,timeout, f"{find_template}")

        # Find the "Delete" menu item within the context menu
        delete_menu_item = driver.find_element(By.XPATH, ".//div[@data-auto='delete']")

        # Scroll into view of the "Delete" menu item
        if delete_menu_item:
            driver.execute_script("arguments[0].scrollIntoView(true);", delete_menu_item)

            # Click on the "Delete" menu item
            delete_menu_item.click()

            yes_button = driver.find_element(By.XPATH, '//button[@data-auto="yes-button"]')
            yes_button.click()


def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = setup_options()
    login(driver, timeout, add_username, add_password)
    click_page_section(driver,timeout)
    click_popups_section(driver,timeout)

    list = ["VAFX2192025","VAFX2192026"]
    for mls in list:
        duplicate_entry(driver,timeout, mls)
    #2.    rename_template = f"TT: {mls}"
    #2.    rename_entry(driver,timeout, mls, rename_template)
    #3.    delete_entry(driver,timeout,mls)
        
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()

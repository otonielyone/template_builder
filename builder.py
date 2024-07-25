import asyncio
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from iframe import create_rental_entry_button

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
    
    try:
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
        
    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        raise  # Reraise the exception to indicate login failure

async def pages_section(driver, timeout):
    txt = '//label[text()="Pages"]'
    pages_section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, txt)))
    pages_section.click()

async def click_popups_section(driver, timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Popups"]')))
    except TimeoutException:
        print("Timed out waiting for Popups section to load")
        raise  # Reraise the exception to indicate section load failure

    click_popups_section = driver.find_element(By.XPATH, '//span[text()="Popups"]')
    click_popups_section.click()

async def click_pages_section(driver, timeout):
    try:
        page_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Pages"]')))
    except TimeoutException:
        print("Timed out waiting for Popups section to load")
        raise  # Reraise the exception to indicate section load failure

    page_element.click()

async def click_rental_page(driver, timeout):
    try:
        rentals_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='RENTALS']"
)))
    except TimeoutException:
        print("Timed out waiting for Popups section to load")
        raise  # Reraise the exception to indicate section load failure

    rentals_element.click()

async def find_template_settings(driver, timeout, template):
    try:
        label_element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, f'//label[text()="{template}"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", label_element)

        next_sibling = label_element.find_element(By.XPATH, './following-sibling::*[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_sibling)
        next_sibling.click()
        
    except TimeoutException:
        print(f"Timed out waiting for template settings: {template}")
        raise  # Reraise the exception to indicate template settings load failure

    except Exception as e:
        print(f"Error occurred during finding template settings: {e}")
        raise  # Reraise the exception to indicate unexpected error

async def duplicate_entry(driver, timeout, mls):
    try:
        await find_template_settings(driver, timeout, "Template Listing")

        txt = "div[data-auto='duplicate'] span"
        duplicate_menu_item = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, txt)))
        driver.execute_script("arguments[0].scrollIntoView(true);", duplicate_menu_item)
        duplicate_menu_item.click()

        new_label_text = f"TT: {mls[0]}"
        input_element_xpath = f"//input[@value='Copy of Template Listing']"
        input_element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, input_element_xpath)))
        input_element.clear()
        input_element.send_keys(new_label_text)
        
        duplicate_me = driver.find_element(By.XPATH, '//div[@role="button"]')
        duplicate_me.click()

    except Exception as e:
        print(f"Error occurred during duplicate entry for MLS {mls[0]}: {e}")
        raise  # Reraise the exception to indicate unexpected error

async def create_popup_templates(mls_list, timeout):
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = await setup_driver()

    await login(driver, timeout, add_username, add_password)
    await pages_section(driver, timeout)
    await click_popups_section(driver, timeout)
    try:
        tasks = []
        for mls in mls_list:
            tasks.append(duplicate_entry(driver, timeout, mls))
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"itetration execution failed: {e}")
    
    finally:
        await pages_section(driver, timeout)
        await click_pages_section(driver, timeout)
        await click_rental_page(driver, timeout)
        await create_rental_entry_button(mls_list, timeout, driver)
        await asyncio.sleep(10)  # Ensure all tasks are completed
        driver.quit()


# Entry point
if __name__ == "__main__":
    timeout = 20
    mls_list = [
        ['VAFX2177404', '4415 Briarwood Ct N #53, Annandale, VA 22003', 2000.0, 'Move-in ready. 2 Bedroom & One Full bathroom, Large living room. Sliding door to generous size private balcony .New Painting, Newer windows & New Curtains, Samsung NEW Dishwasher , Refrigerator & Ice maker , Microwave, Stove-Range-Gas. Elevator and intercom system. Laundry room on same level. Extra storage on the ground floor. 2 parking permits. Condo fees include Heating, gas & water. Close to 495, metro bus stop, shopping center, Restaurants.', 'Active'],
        ['VAPW2069168', '12626 Kahns Rd #B, Manassas, VA 20112', 2000.0, "Be the first to experience this brand-new, fully renovated, bright basement apartment! Nestled in an established neighborhood, there's room to spread out but you&#x2019;re close to convenient shopping plazas and delicious restaurants. Step onto sleek, modern flooring that's as durable as it is stunning, providing the perfect foundation for your décor dreams. Whip up culinary masterpieces in style on the granite countertops, a cooktop and a full-sized fridge, this kitchen is every chef's dream come true! All appliances are brand new. Retreat to one of two cozy bedrooms, each providing a haven of relaxation after a long day. Ample natural light streams through the windows, creating a warm and inviting ambiance. Sip your morning coffee or unwind on your own secluded patio. Escape the hustle and bustle in this peaceful haven, surrounded by nature's beauty. This is a gotta see!", 'Active'],
        ['VAFX2165076', '10600 Rosehaven St, Fairfax, VA 22030', 2000.0, 'LOCATION! LOCATION! Beautiful freshly renovated basement only , located at 66 & 123. Over 1700 square feet of elegance. One large size master bedroom and one full bathroom, large living area, kitchen, washer and dryer. Separate entrance. Rent includes utilities .', 'Active']
    ]
    asyncio.run(create_popup_templates(mls_list, timeout))





'''
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
'''


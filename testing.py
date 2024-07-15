import time

import pytest
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def browser():
    # Initialize WebDriver instance
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

@pytest.fixture
def login_user_web(browser):
    browser.get("URL")  # Replace with your login page URL
    username_field = browser.find_element(By.XPATH, "//input[@id='mat-input-0']")
    password_field = browser.find_element(By.XPATH, "//input[@id='mat-input-1']")
    submit_button = browser.find_element(By.XPATH, "//button[@type='submit' and @class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base']")

    # Enter credentials
    username_field.send_keys("username")
    password_field.send_keys("password")

    # Click submit button
    submit_button.click()

def test_successful_login(browser):
    browser.get("URL")  # Replace with your login page URL
    username_field = browser.find_element(By.XPATH, "//input[@id='mat-input-0']")
    password_field = browser.find_element(By.XPATH, "//input[@id='mat-input-1']")
    submit_button = browser.find_element(By.XPATH, "//button[@type='submit' and @class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base']")

    # Enter credentials
    username_field.send_keys("username")
    password_field.send_keys("password")

    # Click submit button
    submit_button.click()
    WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))
    assert "dashboard" in browser.current_url
    browser.quit()


def test_unsuccessful_login(browser):
    browser.get("URL")  # Replace with your login page URL
    username_field = browser.find_element(By.XPATH, "//input[@id='mat-input-0']")
    password_field = browser.find_element(By.XPATH, "//input[@id='mat-input-1']")
    submit_button = browser.find_element(By.XPATH, "//button[@type='submit' and @class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base']")

    # Enter credentials
    username_field.send_keys("username")
    password_field.send_keys("password")

    # Click submit button
    submit_button.click()
    try:
        WebDriverWait(browser, 5).until(EC.url_contains("dashboard"))
        assert False, "Login was unexpectedly successful"
    except TimeoutException:
        assert "authentication" in browser.current_url
        assert browser.find_element(By.XPATH, "//div[@class='mat-mdc-snack-bar-label mdc-snackbar__label']").text == "Please provide valid username and password"
    browser.close()

def test_logout(browser):
    browser.get("URL")
    try:
        logout_button = browser.find_element(By.XPATH, "//button[@class='sign-button mdc-button mdc-button--unelevated mat-mdc-unelevated-button mat-unthemed mat-mdc-button-base']")
        logout_button.click()
        assert False, "Unsuccessful logout"
    except NoSuchElementException as e:
        assert "authentication" in browser.current_url
    browser.close()


def test_logout_after_login(browser, login_user_web):
    time.sleep(5)
    try:
        dropdown_button = browser.find_element(By.XPATH, "//button[@class='mat-mdc-menu-trigger user-button mdc-fab mdc-fab--mini mat-mdc-mini-fab mat-primary mat-mdc-button-base']").click()
        logout_button = browser.find_element(By.XPATH,
                                             "//button[@class='sign-button mdc-button mdc-button--unelevated mat-mdc-unelevated-button mat-unthemed mat-mdc-button-base']")
        logout_button.click()
        time.sleep(2)
        assert "authentication" in browser.current_url

    except NoSuchElementException as e:
        assert False, "Unsuccessful logout"
    browser.quit()


@pytest.fixture
def open_master_section(browser, login_user_web):
    time.sleep(10)
    master_section = browser.find_element(By.XPATH, "//span[contains(@class, 'mat-content ng-tns-c269005172')]")
    master_section.click()


def test_navigation(browser, login_user_web):
    time.sleep(5)
    master_section = browser.find_element(By.XPATH, "//span[contains(@class, 'mat-content ng-tns-c269005172')]")
    master_section.click()

    roles = browser.find_elements(By.XPATH, "//a[@class='mat-mdc-list-item mdc-list-item mat-mdc-list-item-interactive submenu-list mat-mdc-list-item-single-line mdc-list-item--with-one-line ng-star-inserted' and contains(@href, 'master')]")
    for role in roles:
        role_name = role.find_element(By.XPATH, "./span/span").text.strip().split("\n")[-1]
        role.click()
        time.sleep(2)
        title = browser.current_url.split("/")[-1].capitalize()
        print(f"Role : {role_name}, Title: {title}")
        names = [title, title.split("s")[0]]
        assert role_name in names
    browser.close()

def test_instrument_addition(browser, login_user_web, open_master_section):
    instrument_role = browser.find_element(By.XPATH,
                                  "//a[@class='mat-mdc-list-item mdc-list-item mat-mdc-list-item-interactive submenu-list mat-mdc-list-item-single-line mdc-list-item--with-one-line ng-star-inserted' and contains(@href, 'master/instrument')]")

    time.sleep(2)
    instrument_role.click()
    time.sleep(5)

    add_instrument_button = browser.find_element(By.XPATH, "//button[contains(@class,'mat-mdc-tooltip-trigger mdc-fab mdc-fab--mini mat-mdc-mini-fab mat-primary ng-tns-c4132165266')]")
    add_instrument_button.click()
    time.sleep(5)
    serial_element = browser.find_element(By.XPATH, "//input[@id='mat-input-3']")
    serial_element.send_keys("123")
    time.sleep(5)
    buttons = browser.find_elements(By.XPATH, "//button[@class='mat-mdc-tooltip-trigger mdc-button mdc-button--outlined mat-mdc-outlined-button mat-primary mat-mdc-button-base ng-star-inserted'] ")
    alias_name_create_button = [i for i in buttons if 'Make' in i.get_attribute('mattooltip')]
    alias_name_create_button[0].click()

    div_element = browser.find_element(By.XPATH, "//div[contains(@class,'mat-mdc-form-field-infix ng-tns-c1205077789')]")

    make_name = browser.find_element(By.XPATH, "//input[@id='mat-input-8']")
    make_name.send_keys("Make 0x")
    time.sleep(4)
    
    make_save_button = browser.find_element(By.XPATH, "//form[contains(@class, 'ng-dirty ng-valid ng-touched') or contains(@class, 'ng-pristine ng-invalid ng-touched')]/mat-dialog-actions/button[@class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base ng-star-inserted']")

    make_save_button.click()
    time.sleep(4)
    buttons = browser.find_elements(By.XPATH,
                                    "//button[@class='mat-mdc-tooltip-trigger mdc-button mdc-button--outlined mat-mdc-outlined-button mat-primary mat-mdc-button-base ng-star-inserted'] ")
    model_name_create_button = [i for i in buttons if 'Model' in i.get_attribute('mattooltip')]
    
    model_name_create_button[0].click()
    model_name = browser.find_element(By.XPATH, "//input[@id='mat-input-7']")
    model_name.send_keys("Model 56")
    model_save_button = browser.find_element(By.XPATH,
                         "//form[@class='ng-invalid ng-dirty ng-touched']/mat-dialog-actions/button[@class='mdc-button mdc-button--raised mat-mdc-raised-button mat-primary mat-mdc-button-base ng-star-inserted']")

    model_save_button.click()
    

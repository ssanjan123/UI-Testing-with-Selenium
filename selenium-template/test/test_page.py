import contextlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from e1utils import construct_headless_chrome_driver, get_landing_page_url, wait_for_page_load
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def secret_load(driver):
    try:
        secret = WebDriverWait(driver, 10).until(
            expected_conditions.title_is("SECRET Simple Web Page"))
    except TimeoutException:
        return False
    return True


def NonSecret_check_exists_by_ID(driver):
    try:
        driver.find_element("id", "secretButton")
    except NoSuchElementException:
        return True
    return False


def Secret_check_exists_by_ID(driver):
    try:
        driver.find_element("id", "secretButton")
    except NoSuchElementException:
        return False
    return True


def test_nonsecret_scenario():
    landing_page = get_landing_page_url()
    chrome_driver = construct_headless_chrome_driver()
    # get page
    chrome_driver.get(landing_page)
    # wait for main page to load
    wait_for_page_load(chrome_driver)

    # input name, food and secret code
    name_text = "Dummy"
    food_text = "Ramen"
    password_text = "tragic"
    name_text_field = chrome_driver.find_element("id", "preferredname")
    name_text_field.send_keys(name_text)
    food_text_field = chrome_driver.find_element("id", "food")
    food_text_field.send_keys(food_text)
    password_text_field = chrome_driver.find_element("id", "secret")
    password_text_field.send_keys(password_text)
    chrome_driver.find_element("id", "submit").click()

   # Check if the response page is loaded
    assert 'response.html' in chrome_driver.current_url

    # testing the cases
    test_name = chrome_driver.find_element("id", "thankname").text
    assert test_name == name_text
    test_food = chrome_driver.find_element("id", "foodploy").text
    assert test_food == food_text

    # test if button exists - should not exist here -
    # returns true for not finding the secret button else would fail
    assert NonSecret_check_exists_by_ID(chrome_driver)

    chrome_driver.quit()


def test_secret_scenario():
    landing_page = get_landing_page_url()
    chrome_driver = construct_headless_chrome_driver()
    # get page
    chrome_driver.get(landing_page)
    # wait for main page to load
    wait_for_page_load(chrome_driver)

    # input name, food and secret code
    name_text = "DummySecret"
    food_text = "Noodles"
    password_text = "abracadabra"
    name_text_field = chrome_driver.find_element("id", "preferredname")
    name_text_field.send_keys(name_text)
    food_text_field = chrome_driver.find_element("id", "food")
    food_text_field.send_keys(food_text)
    password_text_field = chrome_driver.find_element("id", "secret")
    password_text_field.send_keys(password_text)
    old_page = chrome_driver.find_element(By.TAG_NAME, 'html')

    chrome_driver.find_element("id", "submit").click()

    # wait for response page to load

    wait_for_page_load(chrome_driver)
    # testing the cases
    # Check if the response page is loaded
    assert 'response.html' in chrome_driver.current_url
    test_name = chrome_driver.find_element("id", "thankname").text
    assert test_name == name_text
    test_food = chrome_driver.find_element("id", "foodploy").text
    assert test_food == food_text

    # Check if the button exists - should exist for secret test
    # returns true for finding the secret button else would fail
    assert Secret_check_exists_by_ID(chrome_driver)

    chrome_driver.find_element("id", "secretButton").click()

    # wait for secret page to load

    assert secret_load(chrome_driver)
    check_secret_name = chrome_driver.find_element("id", "thankname").text
    assert check_secret_name == name_text

    # Check for secret code -- timeout of 10 seconds
    assert chrome_driver.find_element("id", "secret").text == password_text
    chrome_driver.quit()


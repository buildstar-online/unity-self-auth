#!/usr/bin/python3
import sys
import os
import time
import io_tools as io
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

tmp_file_dir = "html_reference"

license_file = sys.argv[1]
license_path = os.getcwd() + license_file

config_file = sys.argv[2]
config_path = os.getcwd() + config_file


class radio_button():
    Name = ""
    xpath = ""
    text = ""


class config():
    elements = {}
    urls = {}


def element_by_xpath(driver, xpath, debug=False):
    try:
        wait = WebDriverWait(driver, timeout=6)
        element = driver.find_elements(By.XPATH, xpath)
        io.print_pretty(f"lookup successfull: found {element} using the path: {xpath}", debug)
        return element[0]
    except Exception as err:
        io.print_pretty(f"cant find the element w/ xpath {xpath}", True)
        print_page(driver, "element_by_xpath_error")
        return err


def element_by_id(driver, elementId, debug=False):  # returns html element
    try:
        element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, elementId)))
        io.print_pretty(f"lookup successfull: found {element} using the id: {elementId}", debug)
        return element
    except Exception as err:
        io.print_pretty(f"cant find the elemtn w/ path {elementId}", True)
        print_page(driver, "element_by_id_error", True)
        return err


def click_on_ready(driver, element, debug=True):
    try:
        wait = WebDriverWait(driver, 6)
        wait.until(ec.element_to_be_clickable(element))
        element.click()
        io.print_pretty(f"click successful on element {element}", True)
    except Exception as err:
        io.print_pretty(f"click failed on element {element}", True)
        print_page(driver, "click_element_error", True)

def login(driver, settings, debug=False):

    # get to unity id login page
    driver.get(settings['urls']['login'])

    # populate the username field
    usn = settings['user']['username']
    usn_element = settings['config']['email_elementId']
    username_element = element_by_id(driver, usn_element, debug)
    username_element.send_keys(usn)

    # populate the password field
    psw = settings['user']['password']
    psw_element = settings['config']['password_elementId']
    password_element = element_by_id(driver, psw_element, debug)
    password_element.send_keys(psw)

    # click the login button
    button_name = settings['config']['login_button']
    login_button = element_by_xpath(driver, button_name)
    click_on_ready(driver, login_button, debug)

    # driver.find_element_by_xpath(settings['config']['login_button']).click()


def unity_auth_upload(driver):

    # get the liscence activation page
    driver.get(unity_license_url)
    time.sleep(5)
    print_page(driver, "license_upload")

    # get the file upload element and pass it our license file
    driver.find_element_by_id(file_elementId).send_keys(license_path)

    # submit the file to the unity license server
    # - will redirect you forcibly to the unity account login if you arent using a logged-in session
    webElement = driver.find_element_by_xpath(button_class_name)
    click_only(driver, webElement)


def select_license_type(driver):
    # attempts to select one of the radio button objects
    print_page(driver, "activation_type_selection")
    # get the available options

    # click the Unity Personal option
    # driver.find_element_by_xpath(login_button).click()


def click_only(driver, webElement):
    # generic function to perform a mouse click ONLY on a webElement

    action = ActionChains(driver)
    action.move_to_element(webElement).click(on_element=webElement)
    action.perform()
    time.sleep(2)


def click_and_release(driver, webElement):
    # generic function to perform a mouse click  AND release on a webElement

    action = ActionChains(driver)
    action.move_to_element(webElement).click(on_element=webElement).release(on_element=webElement)
    action.perform()
    time.sleep(2)


def print_page(driver, name, debug=True):
    # print the page source of the dirver to a .html file

    """
    helpful when you need to see the HTML and find the element names because
    the license page will forcefully redirect you if you are not logged in
    """

    path = f"html_reference/{name}.html"
    io.write_file(path, driver.page_source, debug)


def main():                                         # main program
    debug = True
    go_steppy = False

    # run FireFox in headless mode
    opts = webdriver.FirefoxOptions()
    opts.headless = True
    assert opts.headless

    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(10)
    json_data = io.read_file(config_file)
    vars = io.Variables(json_data, debug, go_steppy)
    settings = vars.settings
    io.print_pretty(vars.settings, debug)
    login_page = settings['urls']['login']

    #todo: open ssl encrypt this or put it in a key vaul
    username = settings['user']['username']
    password = settings['user']['password']

    login(driver, settings, debug)
    unity_auth_upload(driver)
    select_license_type(driver)


main()

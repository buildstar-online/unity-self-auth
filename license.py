#!/usr/bin/python3

import sys
import os
import time
import io_tools as io
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

tmp_file_dir = "html_reference"

license_file = sys.argv[1]
license_path = os.getcwd() + "/" + license_file

config_path = os.getcwd() + "/config.json"

class radio_button():
    Name = ""
    xpath = ""
    text = ""


class config():
    elements = {}
    urls = {}


def element_by_xpath(driver, xpath, debug=False):
    """
    This function will search for a webElement by it's Xpath
    """
    try:
        wait = WebDriverWait(driver, timeout=10)
        element = driver.find_elements(By.XPATH, xpath)
        io.print_pretty(f"found {element} using the path: {xpath}", debug)
        return element[0]
    except Exception as err:
        io.print_pretty(f"cant find the element w/ xpath {xpath}", True)
        print_page(driver, "element_by_xpath_error")
        print(err)
        return err


def element_by_id(driver, elementId, debug=False):  # returns html element
    """
    This functions will search for a webElement by it's ID
    """
    try:
        element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.ID, elementId)))
        io.print_pretty(f"found {element} using the id: {elementId}", debug)
        return element
    except Exception as err:
        io.print_pretty(f"cant find the elemtn w/ path {elementId}", True)
        print_page(driver, "element_by_id_error", True)
        print(err)
        return err


def click_on_ready(driver, element, debug=True):
    """
    This function will wait until the specified webElement is in a
    Ready state and then perform a click action.
    """
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(ec.element_to_be_clickable(element))
        element.click()
        io.print_pretty(f"click successful on element {element}", True)
    except Exception as err:
        io.print_pretty(f"click failed on element {element}", True)
        print_page(driver, "click_element_error", True)
        print(err)
        return err


def login(driver, settings, debug=False):
    """
    This function will open the unity login page and attempt to
    authenticate using the provided credentials. This provides the session
    we will use throughout the authentication process.
    """

    # get to unity id login page
    io.print_pretty('Loading the unity login page...', debug)
    driver.get(settings['urls']['login'])

    # populate the username field
    io.print_pretty('Populating the username field...', debug)
    usn = os.getenv('USERNAME')
    usn_element = settings['config']['email_elementId']
    username_element = element_by_id(driver, usn_element, debug)
    username_element.send_keys(usn)

    # populate the password field
    io.print_pretty('Populating the password field...', debug)
    psw = os.getenv('PASSWORD')
    psw_element = settings['config']['password_elementId']
    password_element = element_by_id(driver, psw_element, debug)
    password_element.send_keys(psw)

    # click the login button
    io.print_pretty('Click the Login Button...', debug)
    wait = WebDriverWait(driver, 5)
    button_name = settings['config']['login_button']
    login_button = element_by_xpath(driver, button_name)
    click_on_ready(driver, login_button, debug)


def unity_auth_upload(driver, settings, debug=False):
    """
    This function will select the Unity .alf file and upload it to the
    authentication service.
    """

    # get the liscence activation page
    io.print_pretty('Load the License Activation Page...', debug)
    driver.get(settings['urls']['license'])

    # get the file upload element and pass it our license file
    # We have to do a sleep here or Unity will clear our inputs
    time.sleep(5)
    io.print_pretty('Looking for the upload field...', debug)
    driver.find_element(By.ID, settings['config']['file_elementId']).send_keys(license_path)
    io.print_pretty("Located the file upload file field.", debug)

    # submit the file to the unity license server
    # will redirect you forcibly to the unity account login if you arent using
    # a logged-in session
    webElement = driver.find_element(
            By.XPATH, settings['config']['button_class_name'])
    io.print_pretty("Located the file upload button.", debug)

    click_only(driver, webElement)
    io.print_pretty("Successfully clicked the upload button", debug)
    select_license_type(driver, settings, debug)


def select_license_type(driver, settings, debug=False):
    """
    This function will select the appropriate options for requesting a
    personal license
    """

    # click the Unity Personal option
    webElement = driver.find_element(
            By.XPATH, settings['radio_buttons']['Personal'])
    click_on_ready(driver, webElement, debug)

    # click an option
    webElement = driver.find_element(
            By.XPATH, settings['radio_buttons']['nosale'])
    click_on_ready(driver, webElement, debug)

    # submit choice
    webElement = driver.find_element(
            By.XPATH, settings['config']['license_options_submit'])
    click_on_ready(driver, webElement, debug)

    time.sleep(2)

    # download the license file to ~/Downloads
    webElement = driver.find_element(
            By.XPATH, settings['config']['download_license']).click()


def click_only(driver, webElement):
    # generic function to perform a mouse click ONLY on a webElement

    action = ActionChains(driver)
    action.move_to_element(webElement).click(on_element=webElement)
    action.perform()
    time.sleep(2)


def click_and_release(driver, webElement):
    # generic function to perform a mouse click  AND release on a webElement

    action = ActionChains(driver)
    action.move_to_element(webElement).click(
            on_element=webElement).release(on_element=webElement)
    action.perform()
    time.sleep(2)


def print_page(driver, name, debug=True):
    # print the page source of the dirver to a .html file

    """
    helpful when you need to see the HTML and find the element names because
    the license page will forcefully redirect you if you are not logged in
    """

    path = f"{name}.html"
    io.write_file(path, driver.page_source, debug)


def main():
    """
    This program will attempt to automatically create, upload,
    and authorize a unity personal licesnse.
    """
    io.print_pretty('Starting...', True)
    
    io.print_pretty('Settig up the web driver...', True)
    opts = webdriver.FirefoxOptions()
    opts.binary_location = '/usr/bin/firefox-esr'

    io.print_pretty('Determining headless status', True)
    headless = os.getenv("HEADLESS", "False") == "True"

    if(headless):
        opts.add_argument("-headless")
        io.print_pretty('Using Headless Mode', True)
    else:
        io.print_pretty('Using Graphical Mode', True)

    # Instantiate the gekko driver
    driver = webdriver.Firefox(executable_path='/home/player1/.local/bin/geckodriver', options=opts)
    driver.implicitly_wait(10)

    # Read settings from jsonfile
    io.print_pretty('Loading Settings...', True)
    debug = True
    go_steppy = False
    json_data = io.read_file(config_path)

    # Convert json data into dict
    vars = io.Variables(json_data, debug, go_steppy)
    settings = vars.settings

    # Perform authentication steps
    io.print_pretty('Starting Login process...', True)
    login(driver, settings, debug)
    
    io.print_pretty('Starting licensing process...', debug)
    unity_auth_upload(driver, settings, debug)
    
    # Wait for fileIO to complete
    io.print_pretty('Saving data...', True)
    time.sleep(2.4)
    from pathlib import Path
    path_to_file = '/home/player1/Downloads/Unity_v2022.x.ulf'
    path = Path(path_to_file)
    if path.is_file():
        io.print_pretty(f'The file {path_to_file} exists', debug)
    else:
        io.print_pretty(f'The file {path_to_file} does not exist', debug)
main()

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 23:02:53 2020

@author: jrslagle
"""

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

driver = webdriver.Chrome()
driver.get("https://rubixdesign.printercloud.com/admin/")
true_username, true_password = ('account1', 'account1')

def main():
    all_passing = True
    
    # Happy path test
    if happy_path(username = true_username, password = true_password):
        print("[PASS] Simple login and logout successful.")
    else:
        print("[FAIL] Simple login failed.")
        print("Ending login test suite early.")
        driver.quit()
        sys.exit(1)

    # Wrong password test
    if bad_login(username = true_username, password = true_password+"$"):
        print("[PASS] Wrong password denied login.")
    else:
        print("[FAIL] Logged in with incorrect password.")
        all_passing = False

    # Wrong username test
    if bad_login(username = true_username+"$", password = true_password):
        print("[PASS] Mistyped username denied login.")
    else:
        print("[FAIL] Logged in with mistyped username.")
        all_passing = False

    # Missing password test
    if bad_login(username = true_username):
        print("[PASS] Missing password denied login.")
    else:
        print("[FAIL] Logged in with missing password.")
        all_passing = False

    # Missing username test
    if bad_login(password = true_password):
        print("[PASS] Missing username denied login.")
    else:
        print("[FAIL] Logged in with missing username.")
        all_passing = False

    # Missing username and password test
    if bad_login():
        print("[PASS] Missing username and password denied login.")
    else:
        print("[FAIL] Logged in with missing username and password.")
        all_passing = False
    
    if all_passing:
        print("\n[PASS] All login tests pass. Login screen performs as designed.")
    else:
        print("\n[FAIL] One or more login tests have failed.")

    driver.quit()
    # test script ends here


def happy_path(username, password):
    site_login(username, password)
    if is_logged_in():
        site_logout()
        return True
    else:
        return False

def bad_login(username = None, password = None):
    site_login(username, password)
    if is_logged_in():
        site_logout()
        return False
    else:
        return True

def site_login(username, password):
    try:
        username_field = driver.find_element_by_id("relogin_user")
        username_field.clear()
        if username != None:
            username_field.send_keys(username)

        password_field = driver.find_element_by_id("relogin_password")
        password_field.clear()
        if password != None:
            password_field.send_keys(password)

        driver.find_element_by_id("admin-login-btn").click()

    except NoSuchElementException:
        print("Couldn't find page elements while trying to log in.")

    except:
        print("Other exception occured while trying to log in:")
        print(sys.exc_info())


def is_logged_in():
    try:
        # wait for 5 seconds for the user menu to show up
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, find_text(true_username)))
        )
        return True
    except TimeoutException:
        # Cannot find user menu. You must not be logged in.
        return False
    except:
        print("Other exception occured while looking for user menu:")
        print(sys.exc_info())

def site_logout():
    try:
        driver.find_element_by_xpath(find_text(true_username)).click()
        driver.find_element_by_xpath(find_text("Log Out")).click()

    except NoSuchElementException:
        print("Couldn't find the User Menu or Log Out button while trying to log out.")

    except:
        print("Other exception occured while trying to log out:")
        print(sys.exc_info())


def find_text(text):
    return "//*[contains(text(), '"+text+"')]"

def save_html(filename):
    with open(filename,'w', encoding="utf-8") as f:
        f.write(driver.page_source)

main()

# TODO:
# click Lost Password
# click Privacy Policy
# are there any other available elements to interact with
# convert test-login to a class with driver, true_username, and true_password as instance variables.
# write a reliable is_logged_out() method.
# run whole login test suite in parallel and see if that's faster.

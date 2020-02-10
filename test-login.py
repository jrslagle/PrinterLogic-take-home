# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 23:02:53 2020

@author: jrslagle
"""

import sys
import time
from selenium import webdriver # is chromedriver in my path?
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

def main():
    username, password = ('account1', 'account1')
    try:    
        happy_path(username, password)
        print("[PASS] Simple login successful.")
    except:
        print("Exception:", sys.exc_info()[1])
        print("[FAIL] Simple login failed.")
        driver.quit()
        sys.exit(1)
        
    try:
        wrong_password(username, password+"$")
        print("[PASS] Correct password required.")
    except:
#        print("Exception:", sys.exc_info()[1])
        print("[FAIL] Logged in with incorrect password.")
    
    driver.quit()


def site_login(username,password):
    driver.get ("https://rubixdesign.printercloud.com/admin/")
    driver.find_element_by_id("relogin_user").send_keys(username)
    driver.find_element_by_id("relogin_password").send_keys(password)
    driver.find_element_by_id("admin-login-btn").click()
    
def happy_path(username, password):
    
    site_login(username, password)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, find_text(username)))
    ).click()
    
    driver.find_element_by_xpath(find_text("Log Out")).click()
        
def wrong_password(username, password):
    
    site_login(username, password)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, find_text(username)))
        )
    except:
        return
        
    raise BaseException
        
def find_text(text):
    return "//*[contains(text(), '"+text+"')]"

main()

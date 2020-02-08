# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 23:02:53 2020

@author: jrslagle
"""

from selenium import webdriver # is chromedriver in my path?
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait WebDriverWait(driver, 10).until(EC.title_contains("home"))

driver = webdriver.Chrome()

def main():
    site_login(username="account1", password="account1")
#    save_html("afterlogin_html.txt")
    print("Yay, we logged in!")

def site_login(username,password):
    driver.get ("https://rubixdesign.printercloud.com/admin/")
    driver.find_element_by_id("relogin_user").send_keys(username)
    driver.find_element_by_id("relogin_password").send_keys(password)
    driver.find_element_by_id("admin-login-btn").click()

def save_html(filename):
    with open(filename,'w', encoding="utf-8") as f:
        f.write(driver.page_source)

main()

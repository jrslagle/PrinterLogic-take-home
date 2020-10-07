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
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

class LoginTests(object):

    def __init__(self, a_username, a_password):
        self.true_username = a_username
        self.true_password = a_password
        self.true_url = 'https://rubixdesigns.printercloud.com/admin/'

    def run_tests(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.true_url)
        all_passing = True
        
        # Happy path test
        if self.happy_path(a_username = self.true_username,
                           a_password = self.true_password):
            print("[PASS] Simple login and logout successful.")
        else:
            print("[FAIL] Simple login failed.")
            print("Ending login test suite early.")
            self.driver.quit()
            sys.exit(1)
    
        # Wrong password test
        if self.bad_login(a_username = self.true_username,
                          a_password = self.true_password+"$"):
            print("[PASS] Wrong password denied login.")
        else:
            print("[FAIL] Logged in with incorrect password.")
            all_passing = False
            
        # Wrong username test
        if self.bad_login(a_username = self.true_username+"$",
                          a_password = self.true_password):
            print("[PASS] Mistyped username denied login.")
        else:
            print("[FAIL] Logged in with mistyped username.")
            all_passing = False
    
        # Missing password test
        if self.bad_login(a_username = self.true_username):
            print("[PASS] Missing password denied login.")
        else:
            print("[FAIL] Logged in with missing password.")
            all_passing = False
    
        # Missing username test
        if self.bad_login(a_password = self.true_password):
            print("[PASS] Missing username denied login.")
        else:
            print("[FAIL] Logged in with missing username.")
            all_passing = False
    
        # Missing username and password test
        if self.bad_login():
            print("[PASS] Missing username and password denied login.")
        else:
            print("[FAIL] Logged in with missing username and password.")
            all_passing = False
        
        # Lost Password test
        if self.lost_password():
            print("[PASS] Lost Password link takes you to password reset screen.")
        else:
            print("[FAIL] Lost Password link does not function correctly.")
            all_passing = False
        
        if self.privacy_policy():
            print("[PASS] Privacy Policy link takes you to Privacy Policy screen.")
        else:
            print("[FAIL] Privacy Policy link does not function normally.")
            all_passing = False
            
        # Conclusion: If any are not passing, then the test suite fails.
        if all_passing:
            print("\n[PASS] All login tests pass. Login screen performs as designed.")
        else:
            print("\n[FAIL] One or more login tests have failed.")
    
        self.driver.quit()
        # test script ends here
    
    
    def happy_path(self, a_username = None, a_password = None):
        run_alone = False
        if a_username == None:
            a_username = self.true_username
            run_alone = True
        if a_password == None:
            a_password = self.true_password
            
        # if running alone, a new web driver is needed
        if run_alone:
            self.driver = webdriver.Chrome()
            self.driver.get(self.true_url)
            
        self.site_login(a_username, a_password)
        if self.is_logged_in():
            self.site_logout()
            if run_alone:    
                print("[PASS] Simple login and logout successful.")
                self.driver.quit()
            else:
                return True
        else:
            if run_alone:
                print("[FAIL] Simple login failed.")
                self.driver.quit()
            else:
                return False
    
    def bad_login(self, a_username = None, a_password = None):
        self.site_login(a_username, a_password)
        if self.is_logged_in():
            self.site_logout()
            return False
        else:
            return True
    
    def lost_password(self):
        # find and click on Lost Password link
        try:
            self.driver.find_element_by_id("forgot-password").click()
            self.driver.find_element_by_id("password-body")
            return True
    
        except NoSuchElementException:
            print("Couldn't find page elements while trying to test Lost Password.")
            return False
    
        except:
            print("Other exception occured while trying to test Lost Password:")
            print(sys.exc_info())
    
        finally:
            self.driver.back()
        
    def privacy_policy(self):
        try:
            self.driver.find_element_by_xpath(find_text("Privacy Policy")).click()
            self.driver.switch_to.window(window_name = self.driver.window_handles[-1])
            if self.driver.title == "Privacy Policy | PrinterLogic":
                self.driver.close()
                self.driver.switch_to.window(window_name = self.driver.window_handles[-1])
                return True
            else:
                return False
    
        except NoSuchElementException:
            print("Couldn't find page elements while trying to test Privacy Policy.")
            print(sys.exc_info())
            return False
            
        except WebDriverException:
            print("This exception is only thrown intermittendly. It might be",
                  "thrown when the driver attempts to move to a new tab before",
                  "it has a chance to load.")
            print(self.driver.window_handles)
            print(sys.exc_info())
    
        except:
            print("Other exception occured while trying to test Privacy Policy:")
            print(sys.exc_info())
    
    def site_login(self, a_username, a_password):
        try:
            username_field = self.driver.find_element_by_id("relogin_user")
            username_field.clear()
            if a_username != None:
                username_field.send_keys(a_username)
    
            password_field = self.driver.find_element_by_id("relogin_password")
            password_field.clear()
            if a_password != None:
                password_field.send_keys(a_password)
    
            self.driver.find_element_by_id("admin-login-btn").click()
            
        except NoSuchElementException:
            print("Couldn't find page elements while trying to log in.")
            
        except StaleElementReferenceException:
            print("Tried to use an element that no longer exists while signing in.")
    
        except:
            print("Other exception occured while trying to log in:")
            print(sys.exc_info())
    
    
    def is_logged_in(self):
        try:
            # wait for 5 seconds for the user menu to show up
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, find_text(self.true_username)))
            )
            return True
        except TimeoutException:
            # Cannot find user menu. You must not be logged in.
            return False
        except:
            print("Other exception occured while looking for user menu:")
            print(sys.exc_info())
    
#    def is_logged_out(self):
#        try:
#            # wait for 5 seconds for "jstree-marker" to show up
#            # this is unique to the login screen
#            WebDriverWait(self.driver, 5).until(
#                EC.presence_of_element_located((By.ID, "jstree-marker"))
#            )
#            return True
#        except TimeoutException:
#            # Cannot find user menu. You must not be logged in.
#            return False
#        except:
#            print("Other exception occured while looking for user menu:")
#            print(sys.exc_info())
    
    def site_logout(self):
        try:
            self.driver.find_element_by_xpath(find_text(self.true_username)).click()
            self.driver.find_element_by_xpath(find_text("Log Out")).click()
    
        except NoSuchElementException:
            print("Couldn't find the User Menu or Log Out button while trying to log out.")
    
        except:
            print("Other exception occured while trying to log out:")
            print(sys.exc_info())
    
    def save_html(self, filename):
        with open(filename,'w', encoding="utf-8") as f:
            f.write(self.driver.page_source)
    
def find_text(text):
    return "//*[contains(text(), '"+text+"')]"

# TODO:
# write a reliable is_logged_out() method.
# run whole login test suite in parallel and see if that's faster.

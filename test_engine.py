# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 22:45:19 2020

@author: jrslagle
"""
from testscripts.logintests import LoginTests

login_test_suite = LoginTests('account1','account1')

#print("Running whole test suite")
login_test_suite.run_tests()

#print("Testing just the happy path without arguments")
#login_test_suite.happy_path()


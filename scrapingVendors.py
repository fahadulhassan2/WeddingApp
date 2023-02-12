from selenium import webdriver
import json
import time
import csv
import pandas as pd
from openpyxl import load_workbook

from csv import writer

## START_OF_DATA_SCRAPPING
class VendorsData(object):
    def __init__(self):
        self.vendorName = ""
        self.vendorUrlName = ""
        self.vendorImageLink = ""
        self.vendorCategory = ""
        self.vendorLocation = ""
        self.vendorAbout = ""
        self.vendorEmail = ""
        self.vendorPhone = ""
        self.vendorWebsite = ""
        self.vendorInstagram = ""
        self.vendorFacebook = ""


def ReadCategoriesAndStoreInDatabase():


# def About():
#     about = browser.find_element_by_class_name("message").text
#     return about
#
#
# def GetData(vendorUrlName, type, data_type):
#     browser.execute_script(
#         "window.open('https://secure-cdn-api.bridestory.com/v2/vendors/" + vendorUrlName + "/action?type=" + type + "&bs-localization-bucket=PK&bs-translation-bucket=en','tab-2')")
#     time.sleep(10)
#     p = browser.current_window_handle
#     # get first child window
#     chwnd = browser.window_handles
#     for w in chwnd:
#         # switch focus to child window
#         if (w != p):
#             browser.switch_to.window(w)
#     try:
#
#         pre = browser.find_element_by_tag_name("pre").text
#         data = json.loads(pre)
#         Data = data[data_type]
#         browser.close();
#         browser.switch_to.window(browser.window_handles[1])
#     except:
#         browser.refresh()
#         time.sleep(10)
#         browser.refresh()
#         pre = browser.find_element_by_tag_name("pre").text
#         data = json.loads(pre)
#         Data = data[data_type]
#         browser.close();
#         browser.switch_to.window(browser.window_handles[1])
#     return Data
#
#
# def Vendors(vendordata):
#     vendor_link = 'https://www.bridestory.com/' + vendordata.vendorUrlName + "?tab=about"
#     browser.execute_script(
#         "window.open('" + vendor_link + "','tab-1')")
#     time.sleep(10)
#     p = browser.current_window_handle
#     # get first child window
#     chwnd = browser.window_handles
#     for w in chwnd:
#         # switch focus to child window
#         if (w != p):
#             browser.switch_to.window(w)
#             break
#
#     vendordata.vendorAbout = About()
#     vendordata.vendorEmail = GetData(vendordata.vendorUrlName, "get_email", "email")
#     vendordata.vendorPhone = GetData(vendordata.vendorUrlName, "get_phone", "phoneNumber")
#     vendordata.vendorWebsite = GetData(vendordata.vendorUrlName, "get_website", "website")
#     vendordata.vendorInstagram = GetData(vendordata.vendorUrlName, "get_instagram", "instagram")
#     vendordata.vendorFacebook = GetData(vendordata.vendorUrlName, "get_facebook", "facebook")
#     print(vendordata.vendorAbout)
#     print(vendordata.vendorEmail)
#     print(vendordata.vendorPhone)
#     print(vendordata.vendorWebsite)
#     print(vendordata.vendorInstagram)
#     print(vendordata.vendorFacebook)
#     browser.close();
#     browser.switch_to.window(browser.window_handles[0])
#     return vendordata


# Login Account

# browser = webdriver.Chrome(executable_path="c:\\selenium\chromedriver.exe")
# browser.get("https://www.bridestory.com/patson-decor")
# browser.find_element_by_class_name("link_login").click()
# browser.implicitly_wait(5)
# browser.find_element_by_name("email").send_keys("bilawal.hussain5646@gmail.com")
# browser.find_element_by_name("password").send_keys("tripleh123")
# browser.find_element_by_class_name("btn-submit").click()
# time.sleep(5)
#
# # Loop here for product
#
# with open('categories.csv', 'r') as categories_file:
#     categories = csv.reader(categories_file)
#     for category in categories:
#         # Create a Pandas Excel writer using XlsxWriter as the engine.
#         current_category = category[0]
#         with open(current_category + '.csv', "w+") as csvFile:
#             writer = csv.writer(csvFile)
#
#
#         with open('thailand vendors.csv', 'r') as vendors_file:
#             vendors_list = csv.reader(vendors_file)
#             # dataframe Name and Age columns
#             with open(current_category + '.csv', "a") as category_file:
#                 writer = csv.writer(category_file)
#                 writer.writerow(['Name',
#                                  'Image',
#                                  'Category',
#                                  'Location',
#                                  'About',
#                                  'Email',
#                                  'Phone',
#                                  'Website',
#                                  'Instagram',
#                                  'Facebook'])
#
#             for vendor in vendors_list:
#
#                 if vendor[3] == current_category:
#                     vendordata = VendorsData()
#
#                     vendordata.vendorName = vendor[0]
#                     vendordata.vendorUrlName = vendor[1]
#                     vendordata.vendorImageLink = vendor[2]
#                     vendordata.vendorCategory = vendor[3]
#                     vendordata.vendorLocation = vendor[4]
#
#                     vendordata = Vendors(vendordata)
#                     with open(current_category + '.csv', "a") as category_file:
#                         writer = csv.writer(category_file)
#                     # new dataframe with same columns
#                         writer.writerow(
#                             [vendordata.vendorName,
#                              vendordata.vendorImageLink,
#                              vendordata.vendorCategory,
#                              vendordata.vendorLocation,
#                              vendordata.vendorAbout,
#                              vendordata.vendorEmail,
#                              vendordata.vendorPhone,
#                              vendordata.vendorWebsite,
#                              vendordata.vendorInstagram,
#                              vendordata.vendorFacebook]
#                         )
# browser.close();


## END OF DATA SCRAPING
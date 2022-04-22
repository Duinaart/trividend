# Scraping and downloading imports
import chromedriver_binary
import requests
import re
import json
import pickle
import time
import os
import pandas as pd


# Scrape and download pdf jaarresultaten robinetto
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# #? Get client names and firm_numbers
xls = pd.read_excel('Opvolgingsdocument Leads.xlsx', 'Klanten')
firm_names = xls['Klant'].to_list()
firm_numbers = xls['Number'].to_list()
print(firm_numbers, firm_names)

for i in range(0, len(firm_numbers)):
    base_folderpath = r'/home/emile/Documents/02 - KUL/3e bachelor/Bachelorproef/jaarrekeningen'
    full_path = os.path.join(base_folderpath,'{}'.format(firm_names[i]))
    options = webdriver.ChromeOptions()
    if not os.path.isdir(full_path):
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
                   "download.default_directory": full_path, "download.extensions_to_open": "applications/pdf"}

        options.add_experimental_option("prefs", profile)
        for j in range(0,15):
            url = 'https://cri.nbb.be/bc9/web/catalog?execution=e2s1'
            company_number = firm_numbers[i]

            driver = webdriver.Chrome(chrome_options=options, executable_path='/home/emile/Documents/02 - KUL/3e bachelor/Bachelorproef/Python/chromedriver')
            driver.get(url)
            driver.maximize_window()

            w1 = WebDriverWait(driver, 8)
            w1.until(EC.presence_of_element_located((By.ID, 'page_searchForm:j_id3:generated_number_2_component')))

            inputElement = driver.find_element_by_id("page_searchForm:j_id3:generated_number_2_component")
            inputElement.send_keys(company_number)
            inputElement.send_keys(Keys.ENTER)

            # Find all the download buttons (0,1,2... : generated_pdfDownload)
            w1.until(EC.presence_of_element_located((By.ID, 'j_idt131:j_idt165:1:generated_pdfDownload_0_cell')))

            # This does not work yet, dropdown button doesn't have id
            # select = Select(driver.find_element_by_xpath('//*[@id="j_idt131:j_idt165"]/div/div[1]/div/div[3]/select'))
            # select.select_by_value('50')
            try:
                driver.find_element_by_id('j_idt131:j_idt165:' + str(j) + ':generated_pdfDownload_0_cell').click()
            except NoSuchElementException:
                break

            # Wait until the files have downloaded
            time.sleep(5)

            driver.quit()





# for firm in firm_names:
#     os.mkdir(os.path.join(base_folderpath,firm))
#     download_dir = os.path.join(base_folderpath,firm)
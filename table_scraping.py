##################################
# Table scraping imports
import os
import glob
import tabula
import pandas as pd
pd.options.display.width = 0
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

# Scraping and downloading imports
import chromedriver_binary
import requests
import re
import json
import pickle
import time
###################################

# Scrape and download pdf jaarresultaten robinetto
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

"""
driver = webdriver.Chrome()

url = 'https://cri.nbb.be/bc9/web/catalog?execution=e2s1'
company_number = '0694.734.685'


driver.get(url)
driver.maximize_window()

w1 = WebDriverWait(driver, 8)
w1.until(EC.presence_of_element_located((By.ID, 'page_searchForm:j_id3:generated_number_2_component')))

inputElement = driver.find_element_by_id("page_searchForm:j_id3:generated_number_2_component")
inputElement.send_keys(company_number)
inputElement.send_keys(Keys.ENTER)

# Find all the download buttons (0,1,2... : generated_pdfDownload)
w1.until(EC.presence_of_element_located((By.ID, 'j_idt131:j_idt165:0:generated_pdfDownload_0_cell')))
driver.find_element_by_id('j_idt131:j_idt165:0:generated_pdfDownload_0_cell').click()

# Wait until the files have downloaded
time.sleep(5)

# Try to change name into 'company number/company name_year'

# -> repeat for every company number in list 
# scrape tables from pdf's 
# put data in excel/csv files for analysis

driver.quit()
"""

########################################################################################
#! Extract tables from pdf and convert to one firm data
#! Make data in such a way that every column has new year with same index of GAAP
########################################################################################
#######################################
#? Activa
######################################
def main():
    files = sorted(glob.glob('/home/emile/Documents/02 - KUL/3e bachelor/Bachelorproef/jaarrekeningen/'
                             'robinetto/*.pdf'))
    final_dfs = []

    for file in files:
        basename = os.path.basename(file)
        current_year = int(basename.split('-')[0]) - 1
        previous_year = int(current_year) - 1

        data = load_data(file)

        final = pd.concat(clean_every_pdf(data, current_year))
        final.reset_index(inplace=True, drop=True)
        final.drop(previous_year, axis=1, inplace=True, errors='ignore')

        final_dfs.append(final)
    final_firm = pd.concat(final_dfs, axis=1, join="inner")
    final_firm = final_firm.loc[:, ~final_firm.columns.duplicated()]
    print(final_firm)


#############################################################################
#? functions
#############################################################################
# Read data from pdf with tabula and make it a df
def load_data(file):
    df_list = []
    for i in range(1,8):
        df1 = tabula.read_pdf(file, output_format='dataframe', pages=i, multiple_tables=True)
        df = df1[0] if len(df1) else pd.DataFrame()
        df_list.append(df)
    df_list2 = [i for i in df_list if i.size >= 50]
    return df_list2

def clean_every_pdf(data, current_year):
    cleaned_dfs = []
    for df in data:
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.dropna(how='all', axis=1)
        df.reset_index(inplace=True)
        df.columns.name = None
        df.drop('Vorig boekjaar', axis=1, inplace=True, errors='ignore')
        df.rename(columns={'Boekjaar': current_year}, inplace=True)
        df.drop('level_1', axis=1, inplace=True)
        df.rename(columns={'level_0': "Beschrijving"}, inplace=True)

        # test to see if it works for every part of the thing
        df.drop('level_2', axis=1, inplace=True, errors='ignore')
        df.rename(columns={'level_3': 'Codes'}, inplace=True, errors='ignore')

        cleaned_dfs.append(df)

    return cleaned_dfs



#############################
#  run
#############################
if __name__ == '__main__':
    main()

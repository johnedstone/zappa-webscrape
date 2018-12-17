'''
AWS Lambda:
https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/blob/master/lambda_function.py
https://medium.com/@manivannan_data/python-selenium-on-aws-lambda-b4b9de44b8e1
http://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/
https://duo.com/decipher/driving-headless-chrome-with-python

Web Scraping:
https://towardsdatascience.com/an-introduction-to-web-scraping-with-python-bc9563fe8860
https://pythonprogramminglanguage.com/web-scraping-with-pandas-and-beautifulsoup/

Login:
https://crossbrowsertesting.com/blog/test-automation/automate-login-with-selenium/

Python Selenium find element by
https://selenium-python.readthedocs.io/locating-elements.html
https://saucelabs.com/resources/articles/selenium-tips-css-selectors

Pandas Dataframe merge and transform:
http://pbpython.com/pandas_transform.html
'''

import os, sys
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as BS
from tabulate import tabulate
import pandas as pd

CHROM_VERBOSITY = 0 # default was 99
URL = os.getenv('URL')
USER = os.getenv('USER')
PW = os.getenv('PW')
DASHBOARD = os.getenv('DASHBOARD') # Can not navigate directly
ORDERS = os.getenv('ORDERS')

def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v={}'.format(CHROM_VERBOSITY))
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
    executable_path = os.getcwd() + '/bin/chromedriver'

    driver = webdriver.Chrome(executable_path=executable_path,
        chrome_options=chrome_options)

    conversion = yaml.load(open('conversion.yaml'))

    try:
        driver.get(URL)
        driver.find_element_by_id('username').send_keys(USER)
        driver.find_element_by_id ('password').send_keys(PW)
        driver.find_element_by_css_selector('button.loginoperation').click()
        driver.get(DASHBOARD)
        driver.find_element_by_css_selector('a[href="{}"]'.format(ORDERS)).click()
        # driver.get(ORDERS) # This could replace the line above
        #print(driver.page_source)

        data = driver.page_source

        # with open('raw.html') as fh:
        #    data = fh.read()

        soup = BS(data,'lxml')
        table = soup.find_all('table')[0]

        df = pd.read_html(str(table))[0]
        last_column = df.columns[len(df.columns)-1]
        df = df.drop([0], axis=0) \
            .drop(columns=['Customer', 'Supply Cost', last_column]) \
            .astype({"Quantity": int})


        conversion_keys = conversion.keys()

        conversion_lists = []
        rows_to_keep = []

        for row in df.itertuples():
            if row[3] in conversion_keys: # if item name == is in conversion yaml
                ## conversion_lists.append(list(row)[1:]) # use this line for testing
                for k in conversion[row[3]].keys(): # get the keys of this item
                    new_row = []
                    new_row.append(row[1])
                    new_row.append(row[2])
                    new_row.append(k)
                    new_row.append(row[4] *  conversion[row[3]][k])
                    conversion_lists.append(new_row)

            else:
                rows_to_keep.append(list(row)[1:])

        updated_df = pd.DataFrame(conversion_lists + rows_to_keep, columns=df.columns)

        output = '''
{}
            
{}
            '''.format(
            updated_df.groupby('Product Title')["Quantity"].sum(),
            tabulate(df, headers='keys', tablefmt='psql')
        )
        print(output)

    finally:
        driver.close()

if __name__ == '__main__':
    main()

# vim: ai et ts=4 sw=4 sts=4 nu ru

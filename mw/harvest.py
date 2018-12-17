# -*- coding: utf-8 -*-
import os, sys
import yaml
from datetime import datetime, timezone
import pytz

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as BS
from tabulate import tabulate
import pandas as pd

from django.conf import settings
from django.shortcuts import render

from .heavy_lifting import heavy_lifting

HUMAN_DATETIME  = "%A, %B %d, %Y at %H:%M:%S %z"

def indy_time():
    '''https://medium.com/@eleroy/10-things-you-need-to-know-about-date-and-time-in-python-with-datetime-pytz-dateutil-timedelta-309bfbafb3f7'''

    tz = pytz.timezone('America/New_York')
    return datetime.now(timezone.utc).astimezone(tz).strftime(HUMAN_DATETIME)


def harvest(request, fancy=True):

    submit_id = indy_time()
    context = {
        'submit_id': submit_id,
    }

    heavy_lifting()
    return render(request, 'mw/results.html', context)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v={}'.format(settings.CHROM_VERBOSITY))
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
        
    try:
        driver.get(settings.URL)
        driver.find_element_by_id('username').send_keys(settings.USER)
        driver.find_element_by_id ('password').send_keys(settings.PW)
        driver.find_element_by_css_selector('button.loginoperation').click()
        driver.get(settings.DASHBOARD)
        driver.find_element_by_css_selector('a[href="{}"]'.format(settings.ORDERS)).click()
        # driver.get(ORDERS) # This could replace the line above
        #print(driver.page_source)

        data = driver.page_source

        submit_id = indy_time()
        context = {
            'submit_id': submit_id,
            }
        return render(request, 'mw/results.html', context)
        
        soup = BS(data,'lxml')
        table = soup.find_all('table')[0]

        df = pd.read_html(str(table))[0]
        last_column = df.columns[len(df.columns)-1]
        df = df.drop([0], axis=0) \
            .drop(columns=['Customer', 'Supply Cost', last_column]) \
            .astype({"Quantity": int})

        # put all this in an async and write to S3
        '''
        conversion = yaml.load(open('conversion.yaml'))
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
        '''

        output = '''
{}
            
{}
            '''.format(
            df.groupby('Product Title')["Quantity"].sum(),
            tabulate(df, headers='keys', tablefmt='psql')
        )

    except Exception as e:
        output = '{}'.format(e)

    finally:
        driver.close()

    if fancy:
        output = '''
<style>
div {{
    margin: 2em;
    color: #005dab;
    font-family:"Lucida Console", Monaco, "Courier New", Courier, monospace;
    white-space:pre;
}}
</style>
<div>{}</div>
'''.format(output)

# vim: ai et ts=4 sw=4 sts=4 nu ru

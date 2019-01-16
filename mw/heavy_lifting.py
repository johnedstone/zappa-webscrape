# -*- coding: utf-8 -*-
import io, os, sys, yaml

from zappa.async import task

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as BS
from tabulate import tabulate
import pandas as pd

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

@task
def banner_page(submit_id='unknown_submit_id',
    results_timestamp='results_timestamp'):

    output = '''
<div>Submit ID: {}</div>
<div class="some_padding">
Your Totals are being calculated and will be available in 2-4 min.
<br>
Click the "Refresh Results" Button shortly to display your results.
</div>
'''.format(submit_id)

    with io.StringIO() as fh:
        fh.write(output)
        path = default_storage.save(
            '{}-{}.html'.format(
                settings.RESULTFILE_NAME,
                results_timestamp),
            ContentFile(fh.getvalue().encode('utf-8')))

@task
def heavy_lifting(submit_id='unknown_submit_id',
    fancy=True, results_timestamp='results_timestamp',
    mw_cron=False):
    ''' Sample:
    with io.StringIO() as fh:
        fh.write('Submit ID; {}'.format(submit_id))
        path = default_storage.save('results.html', ContentFile(fh.getvalue().encode('utf-8')))
    or

    fh = default_storage.open('results.html', 'w')
    fh.write(submit_id)
    fh.close()
    '''

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
        
    is_error = False
    try:
        driver.get(settings.URL)
        driver.find_element_by_id('username').send_keys(settings.USER)
        driver.find_element_by_id ('password').send_keys(settings.PW)
        driver.find_element_by_css_selector('button.loginoperation').click()
        driver.get(settings.DASHBOARD)
        driver.find_element_by_css_selector('a[href="{}"]'.format(settings.ORDERS)).click()
        # driver.get(ORDERS) # This could replace the line above

        data = driver.page_source
        
        soup = BS(data,'lxml')
        table = soup.find_all('table')[0]

        df = pd.read_html(str(table))[0]
        last_column = df.columns[len(df.columns)-1]
        df = df.drop(columns=['Customer', 'Supply Cost', last_column]) \
            .astype({"Quantity": int})

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
        _sum = updated_df.groupby('Product Title')["Quantity"].sum() # this is a series groupby object
        _sum_pretty = pd.DataFrame(_sum).to_html(classes=['table', 'table-striped', 'table-sm'],
                                                 table_id="1",
                                                 border=0,
                                                 justify="left",
                                                 header=False)
        _table = tabulate(df, headers='keys', tablefmt='psql')

        output = '''
{}
            
{}
            '''.format(_sum, _table)

    except Exception as e:
        output = '{}'.format(e)
        is_error = True

    finally:
        driver.close()

    if not is_error and fancy:
        output = '''
<style>
div.mono {{
    margin: 0.2em;
    color: #000;
    font-family:"Lucida Console", Monaco, "Courier New", Courier, monospace;
    white-space:pre;
}}
</style>
<div class="table-responsive">{}</div>
<div class="mono">Submit ID: {}</div>
<div class="mono">{}</div>
'''.format(_sum_pretty, submit_id, _table)

    else:
        output = '''
{}

{}'''.format(submit_id, output)

    if mw_cron:
        results_file_name = 'results.html'
    else:
        results_file_name = '{}-{}.html'.format(
            settings.RESULTFILE_NAME,
            results_timestamp,
            )

    with io.StringIO() as fh:
        fh.write(output)
        path = default_storage.save(results_file_name,
            ContentFile(fh.getvalue().encode('utf-8')))

    return

# vim: ai et ts=4 sw=4 sts=4 nu ru

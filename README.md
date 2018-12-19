# zappa-webscrape
Simple Zappa Webscraping with Selenium, Pandas, and BeautifulSoup

### References
#### AWS Lambda
* https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/blob/master/lambda_function.py
* https://medium.com/@manivannan_data/python-selenium-on-aws-lambda-b4b9de44b8e1
* http://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/
* https://duo.com/decipher/driving-headless-chrome-with-python

#### Web Scraping
* https://towardsdatascience.com/an-introduction-to-web-scraping-with-python-bc9563fe8860
* https://pythonprogramminglanguage.com/web-scraping-with-pandas-and-beautifulsoup/

#### Login
* https://crossbrowsertesting.com/blog/test-automation/automate-login-with-selenium/

#### Python Selenium find element by
* https://selenium-python.readthedocs.io/locating-elements.html
* https://saucelabs.com/resources/articles/selenium-tips-css-selectors

#### Pandas Dataframe merge and transform:
* http://pbpython.com/pandas_transform.html

#### Django and Zappa
* https://github.com/Miserlou/Zappa
* https://edgarroman.github.io/zappa-django-guide/

#### S3 Django
* https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
* http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

##### Problems writing from lambda to S3
* **_Note: The problem is a sessions problem_**
* https://github.com/Miserlou/Zappa/issues/984#issuecomment-313789220
* https://github.com/Miserlou/Zappa/issues/1043
* Based on the above, it's not recommended to have a S3 role, distinct from the zappa role,
though it would be helpful, so as to limit the S3 role.  So, in the end, give the S3 role the
AdministraionAccess privliges, and use this both for deploying zappa and writing to S3

### How to mock a request

```
>>> request_factory = RequestFactory()
>>> request = request_factory.get('/path', data={'name': u'test'})
```

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
* **_Note: The notes here on VPC are not needed, the problem is a sessions problem_**
* Next: https://github.com/Miserlou/Zappa/issues/1043 - this explains the problem
* https://realpython.com/python-boto3-aws-s3/
* Key: https://gist.github.com/reggi/dc5f2620b7b4f515e68e46255ac042a7
* https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-public-private-vpc.html
* https://edgarroman.github.io/zappa-django-guide/aws_network_primer/#general-behavior-and-internet-access 
* https://docs.aws.amazon.com/lambda/latest/dg/vpc.html#vpc-internet
* https://aws.amazon.com/blogs/aws/new-vpc-endpoint-for-amazon-s3/

```
https://stackoverflow.com/questions/35455281/aws-lambda-how-to-setup-a-nat-gateway-for-a-lambda-function-with-vpc-access
setup new subnets for your lambda (with CIDRs not overlapping your existing subnets). You need:
one subnet which will be pointing to an Internet Gateway (IGW) to be used by the NAT (let's call it A)
several pointing to the NAT to be used by your lambda (B, C and D)
add a NAT gateway: set the subnet to A
set your lambda VPC subnets to B, C and D
create 2 routes table:
one that points to your NAT with destination 0.0.0.0/0
one that points to your IGW (should already exists) with destination 0.0.0.0/0
update the subnet A to use the route table pointing to the IGW
update the subnets B, C and D to use the route table pointing to the NAT
```

### How to mock a request

```
>>> request_factory = RequestFactory()
>>> request = request_factory.get('/path', data={'name': u'test'})
```

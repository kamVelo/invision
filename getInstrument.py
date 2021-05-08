from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import JavascriptException,NoSuchElementException, StaleElementReferenceException
from time import sleep
from datetime import datetime as dt
from stock import Stock
import os

def isTradeable_212(stock:Stock):
    """
    this function checks if a stock is available to trade on trading 212.
    :param stock: Stock object
    :return: True/False for if the stock is tradeable or not.
    """
    symbol = stock.ticker
    if dt.now().date().day == 1 or not os.path.isfile("T212Stocks.txt"):
        getT212Stocks()
    record = open("T212Stocks.txt", "r")
    tickers = record.read().split('\n')
    is_tradeable = False
    if symbol in tickers:
        is_tradeable = True
    return is_tradeable
def getT212Stocks():
    opts = Options()  # options class for selenium
    opts.headless = False  # allows me to see the browser
    browser = Chrome(options=opts)  # initiates browser
    browser.get("https://demo.trading212.com/")  # gets the website

    # gets username and password entry boxes and fills with the username and password.

    """this while loop accounts for the loading time regardless of internet speeds"""
    sleep(3)
    loggedIn = False
    while not loggedIn:
        try:
            username = browser.find_element_by_id("username-real")
            username.send_keys("trading213.3@gmail.com")
            password = browser.find_element_by_id("pass-real")
            password.send_keys("Btrbtr12")
            password.submit()
            loggedIn = True
        except JavascriptException:
            print("ERROR")
            pass
    sleep(5)
    browser.find_element_by_id("navigation-search-button").click() #opens search box
    sleep(5)
    browser.find_element_by_css_selector("div[data-folder-key='stocks']").click() #opens up stock folder
    sleep(5)
    # below code clicks finds USA button and clicks it to refine by USA.
    browser.execute_script("document.getElementsByClassName('search-folder')[22].childNodes[0].childNodes[1].childNodes[0].click()")
    sleep(5)
    raw_list = browser.find_elements_by_class_name('search-results-instrument')
    record = open("T212Stocks.txt", "w")
    for el in raw_list:
        data = el.text.split('\n')
        ticker = data[0][data[0].find('(')+1:data[0].find(')')]
        record.write(f"{ticker}\n")
    record.close()
def getMovers():
    """
    this function gets all the biggest upward movers from finviz.com under $5
    :return: list of Stock objects
    """

    # starts browser
    url = "https://finviz.com/screener.ashx?v=171&f=sh_price_5to50,sh_relvol_o2&ft=3&o=-averagetruerange"
    opts = Options()
    opts.headless = False
    browser = Chrome(options=opts)
    browser.get(url)

    # tries to collect all the stocks being shown
    # exception for if the accept cookies button pops up before it has collected all the stocks
    try:
        # dark and light because finviz divides the stocks into two different classes alternately per row
        darkstocks = browser.execute_script("return document.getElementsByClassName('table-dark-row-cp')")
        lightstocks = browser.execute_script("return document.getElementsByClassName('table-light-row-cp')")
    except Exception:  # just in case the cookies pop-up is too quick, clicks on accept
        browser.find_element_by_xpath('//*[@title="Scroll to the bottom of the text below to enable this button"]').click()
    ret_list = []  # list of Stock objects to be appended
    # for loop iterates through length of the stock (assumes both lists are equal length, which they are for now)
    for i in range(0, len(darkstocks)):
        # gets a pair (i.e no. 1 and no.2)
        pair = [darkstocks[i], lightstocks[i]]
        # for both stocks append their Stock objects to the return list.
        for stock in pair:
            data = stock.text.split("\n")
            ret_list.append(Stock(data[1], float(data[10])))
    return ret_list

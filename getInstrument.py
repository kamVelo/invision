from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import JavascriptException,NoSuchElementException, StaleElementReferenceException
from time import sleep
def getStocksOnT212():
    opts=  Options()
    opts.headless= False
    browser = Chrome()
    browser.get("https://demo.trading212.com/")
    loggedIn = False
    while not loggedIn:
        try:
            username = browser.find_element_by_id("username-real")
            username.send_keys("trading213.3@gmail.com")
            password = browser.find_element_by_id("pass-real")
            password.send_keys("Btrbtr12")
            password.submit()
            loggedIn = True
            print("LOGGED IN")
        except JavascriptException:
            print("ERROR")
            pass
    found = False
    while not found:
        try:
            browser.find_element_by_id("navigation-search-button").click()
            found = True
        except NoSuchElementException:
            pass
    found = False
    while not found:
        try:
            browser.find_element_by_xpath('//*[@data-folder-key="stocks"]').click()
            sleep(1)
            browser.find_element_by_xpath('//*[@data-folder-key="usa"]').click()
            found = True
        except NoSuchElementException:
            pass

    element_list = browser.find_elements_by_class_name("search-results-instrument")
    symbols = []
    for el in element_list:
        try:
            symbols.append(el.get_attribute("data-code"))
        except StaleElementException:
            pass
    return symbols

#def isTradeable(symbol:str):

print(getStocksOnT212())
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
        browser.find_element_by_xpath(
            '//*[@title="Scroll to the bottom of the text below to enable this button"]').click()
    pos_list = []  # list of Stock objects to be appended

    # for loop iterates through length of the stock (assumes both lists are equal length, which they are for now)
    for i in range(0, len(darkstocks)):
        # gets a pair (i.e no. 1 and no.2)
        pair = [darkstocks[i], lightstocks[i]]
        # for both stocks append their Stock objects to the return list.
        for stock in pair:
            data = stock.text.split("\n")
            #retlist.append(Stock(data[1], float(data[8]), float(data[9].repl
            pos_list.append([data[1],float(data[8]),float(data[9])])


    #return retlist

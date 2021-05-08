from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import JavascriptException
from string import ascii_letters
def convertNums(datum):
    for i in datum:
        print(i)
class executor():
    """this class is the class for interacting with trading212.com"""
    def __init__(self, symbol):
        """:param symbol of the instrument which is being traded e.g EURUSD or AAPL"""
        self.symbol = symbol
        self.start() #calls the start function


    def start(self):
        """starts the browser using chromedriver and selenium and gathers all necessary Javascript code etc."""
        symbol = self.symbol
        opts = Options() #options class for selenium
        opts.headless = False # allows me to see the browser
        self.browser = Chrome(options=opts) # initiates browser
        self.browser.get("https://demo.trading212.com/") # gets the website

        #gets username and password entry boxes and fills with the username and password.

        """this while loop accounts for the loading time regardless of internet speeds"""
        sleep(3)
        loggedIn = False
        while not loggedIn:
            try:
                username = self.browser.find_element_by_id("username-real")
                username.send_keys("trading213.3@gmail.com")
                password = self.browser.find_element_by_id("pass-real")
                password.send_keys("Btrbtr12")
                password.submit()
                loggedIn = True
            except JavascriptException:
                print("ERROR")
                pass

        #script to get the buy/sell buttons for given symbol
        getButtons = "var box = document.querySelectorAll('[data-code=\""+symbol+"\"]');" \
                     "var sellBtn = box[0].querySelectorAll('[data-dojo-attach-point=\"sellButtonNode\"]')[0];" \
                     "var buyBtn = box[0].querySelectorAll('[data-dojo-attach-point=\"buyButtonNode\"]')[0];" \
                     "return [sellBtn, buyBtn];"
        #script to close an order
        self.close = "var instrument = document.querySelectorAll('[data-code=\""+symbol+"\"]')[1];" \
                "instrument.querySelectorAll('[data-column-id=\"close\"]')[0].click();"

        #script to click accept when click button has been pressed
        self.finalise = "document.querySelectorAll('[data-dojo-attach-point=\"controlsNode\"]')[0].querySelectorAll('[data-dojo-attach-point=\"firstButtonNode\"]')[0].click();"

        #script to return the current unrealised PL
        self.getPL = "return document.querySelectorAll('[data-code=\""+symbol+"\"]')[1].querySelectorAll('[data-column-id=\"ppl\"]')[0].innerText;"

        #script to return the current margin of the position
        self.getMgn = "return document.querySelectorAll('[data-code=\""+symbol+"\"]')[1].getElementsByClassName(\"margin\")[0].innerText;"

        self.getBal = "return document.getElementById(\"equity-total\").childNodes[3].innerText;"

        self.getCPrice = "return document.querySelectorAll('[data-code=\"" + symbol + "\"]')[1].childNodes[5].innerText;"

        self.getOPrice = "return document.querySelectorAll('[data-code=\"" + symbol + "\"]')[1].childNodes[4].innerText;"

        self.changeQuantity = "document.querySelectorAll('[data-code=\""+symbol+"\"]')[0].childNodes[11].childNodes[0].childNodes[3].childNodes[3].childNodes[5].click();" \
                          "list = document.querySelectorAll('[data-code=\""+symbol+"\"]')[0].childNodes[11].childNodes[0].childNodes[3].childNodes[5].childNodes[1].childNodes[1].childNodes[1].childNodes;" \
                        "list[list.length-2].click();"

        self.getQuanPos = "return document.querySelectorAll('[data-code=\""+symbol+"\"]')[1].childNodes[2].innerText"

        """ensures we can get buttons regardless of loading speed."""

        gotBTNS = False
        while not gotBTNS:
            try:
                btns = self.browser.execute_script(getButtons)  # gets the buy and sell btns
                self.sell, self.buy = btns[0], btns[1]  # gets the buttons from list above
                gotBTNS = True
            except JavascriptException:
                pass

    def buyOrder(self):
        """buys amount of the instrument equivalent to about 80% of balance"""
        self.setQuantity()
        sleep(3)
        self.buy.click()

    def sellOrder(self):
        """sells amount of the instrument equivalent to about 80% of balance. """
        self.setQuantity()
        sleep(3)
        self.sell.click()

    def closeOrder(self):
        """closes the position"""
        try:
            self.browser.execute_script(self.close)
        except JavascriptException:
            return False

        finalised = False
        while not finalised:
            try:
                self.browser.execute_script(self.finalise)
                finalised = True
            except JavascriptException:
                pass
        return finalised


    def getProfit(self):
        """:return profit made from position
        :except if there is no position"""
        try:
            return float(self.browser.execute_script(self.getPL).replace(u'\xa0',u''))
        except JavascriptException:
            return None
    def getMargin(self):
        """:return margin on the position open
        :except if there is no position"""
        try:
            return float(self.browser.execute_script(self.getMgn).replace(u'\xa0',u''))
        except JavascriptException:
            return None

    def getCurrentPrice(self):
        """
        :except: if there's an error with the site.
        :return: the price of the instrument
        """
        cur_price = None
        while not cur_price:
            try:
                cur_price =  float(self.browser.execute_script(self.getCPrice).replace(u'\xa0',u''))
            except JavascriptException:
                pass
        return cur_price


    def getOpenPrice(self):
        """
        this gets the price a position was opened at
        :return: the price the position was opened at
        """
        open_price = None
        while not open_price:
            try:
                open_price = float(self.browser.execute_script(self.getOPrice).replace(u'\xa0', u''))
            except JavascriptException:
                pass
        return open_price
    def getBalance(self):
        try:
            return float(self.browser.execute_script(self.getBal).replace('$','').replace(u'\xa0', u''))
        except JavascriptException:
            return None

    def setQuantity(self):
        try:
            self.browser.execute_script(self.changeQuantity)
            return True
        except JavascriptException:
            return None
    def getQuantity(self):
        quantity = None
        while not quantity:
            try:
                quantity = float(self.browser.execute_script(self.getQuanPos).replace(u'\xa0', u''))
            except JavascriptException:
                pass
        return quantity


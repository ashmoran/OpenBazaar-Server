import json
from threading import Thread, Condition
from urllib2 import Request, urlopen, URLError
from datetime import datetime, timedelta


class DashPrice(Thread):
    """
    A class for loading and caching the current Dash exchange price.
    There only needs to be one instance of the class running, use DashPrice.instance() to access it
    """

    @staticmethod
    def instance():
        return DashPrice.__instance

    def __init__(self):
        Thread.__init__(self, name="DashPrice Thread")
        self.prices = {}
        self.condition = Condition()
        self.keepRunning = True
        # self.loadPriorities = ["loadpoloniex", "loadcoinmarketcap"]
        self.loadPriorities = ["loadcoinmarketcap"]
        DashPrice.__instance = self

    def closethread(self):
        self.condition.acquire()
        self.keepRunning = False
        self.condition.notify()
        self.condition.release()

    def get(self, currency, refresh_rates=True):
        """
        :param currency: an upper case 3 letter currency code
        :return: a floating point number representing the exchange rate from BTC => currency
        """
        if refresh_rates:
            self.loadPrices()
        self.condition.acquire()
        try:
            last = self.prices[currency]
        except Exception:
            last = 0
        finally:
            self.condition.release()
        return last

    def run(self):
        minuteInterval = 15

        while self.keepRunning:

            self.condition.acquire()
            self.loadPrices()

            now = datetime.now()
            sleepTime = timedelta(minutes=minuteInterval - now.minute % minuteInterval).total_seconds() - now.second

            self.condition.wait(sleepTime)
            self.condition.release()

        DashPrice.__instance = None

    def loadPrices(self):
        success = False
        for priority in self.loadPriorities:
            try:
                getattr(self, priority)()

                success = True
                break

            except URLError as e:
                print "Error loading " + priority + " url " + str(e)
            except (ValueError, KeyError, TypeError) as e:
                print "Error reading " + priority + " data" + str(e)

        if not success:  # pragma: no cover
            print "DashPrice unable to load Dash exchange price"

    @staticmethod
    def dictForUrl(url):
        request = Request(url)
        result = urlopen(request, timeout=5).read()
        return json.loads(result)

    # def loadpoloniex(self):
    #     for currency, info in self.dictForUrl('https://poloniex.com/public?command=returnTicker').iteritems():

    def loadcoinmarketcap(self):
        data = self.dictForUrl('https://api.coinmarketcap.com/v1/ticker/dash/')
        self.prices["USD"] = data[0]["price_usd"]


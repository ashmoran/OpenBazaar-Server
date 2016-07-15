import time
from twisted.trial import unittest
from market.dashprice import DashPrice


class MarketDashProtocolTest(unittest.TestCase):

    # DASHTODO: identify and test DASH price APIs
    def test_DashPrice(self):
        dashPrice = DashPrice()
        dashPrice.start()
        time.sleep(0.01)
        rate = DashPrice.instance().get("USD")
        self.assertGreater(rate, 0)
        dashPrice.closethread()
        dashPrice.join()

    def test_DashPrice_loadbitpay(self):
        dashPrice = DashPrice()
        dashPrice.loadPriorities = ["loadcoinmarketcap"]
        dashPrice.start()
        time.sleep(0.01)
        rate = dashPrice.get("USD")
        self.assertGreaterEqual(rate, 0)
        dashPrice.closethread()
        dashPrice.join()

    # This one is too complex for, sticking with
    #
    # def test_DashPrice_loadpoloniex(self):
    #     dashPrice = DashPrice()
    #     dashPrice.loadPriorities = ["loadpoloniex"]
    #     dashPrice.start()
    #     time.sleep(0.01)
    #     rate = dashPrice.get("USD")
    #     self.assertGreaterEqual(rate, 0)
    #     dashPrice.closethread()
    #     dashPrice.join()

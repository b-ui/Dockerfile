class Strategy:
    def __init__(self, chan_query):
        self.chan_query = chan_query

    def run(self):
        self.buy()
        self.sell()
        self.cut()

    def buy(self):
        pass

    def sell(self):
        pass

    def cut(self):
        pass


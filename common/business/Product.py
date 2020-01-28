
class Product(object):

    def __init__(self, name, category, prices=None, variations=None, variation_values=None):
        self.name = name
        self.category = category
        self.prices = prices
        self.variations = variations
        self.variation_values = variation_values

    def get_price_range(self):

        if self.prices is not None and len(self.prices):
            ret = '${0} - ${1}'
            return ret.format(self.prices[0], self.prices[1])

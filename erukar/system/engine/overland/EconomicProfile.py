import math, statistics

class EconomicProfile:
    '''Supply and Demand units are literally just a single unit. Demand
    is harder to evaluate but it's preemptive'''
    DemandDecayScalarOnSell = 0.5
    MaxPriceMemoryLength = 10

    def __init__(self, seed_fn=None):
        self.supply = {}
        self.demand = {}
        self.recent_prices = {}
        if seed_fn:
            seed_fn(self)

    def price_scalar(self, good):
        self.guard_entries(good)
        mtype = type(good)
        # No demand!
        delta_q = self.demand[mtype] - self.supply[mtype]
        if delta_q > 10:
            return 1.1 + (delta_q/1000)**2
        return 0.75 + 0.25*(1/math.log10(20-delta_q))

    def register_transaction(self, good, at_price, supply_shift):
        self.guard_entries(good)
        self.supply[type(good)] = max(0, self.supply[type(good)]+supply_shift)
        if supply_shift > 0:
            demand_shift = int(supply_shift*self.DemandDecayScalarOnSell)
            self.demand[type(good)] = max(0, self.demand[type(good)]-demand_shift)
        if supply_shift < 0:
            self.demand[type(good)] = max(0, self.demand[type(good)]-supply_shift)
        self.recent_prices[type(good)].append(at_price)
        if len(self.recent_prices[type(good)]) > self.MaxPriceMemoryLength:
            self.recent_prices[type(good)] = self.recent_prices[type(good)][-self.MaxPriceMemoryLength:]

    def guard_entries(self, good):
        if type(good) not in self.supply: self.supply[type(good)] = 0
        if type(good) not in self.demand: self.demand[type(good)] = 0
        if type(good) not in self.recent_prices: self.recent_prices[type(good)] = []

    def average_transaction_price(self, good):
        scalar = self.price_scalar(good)
        #if len(self.recent_prices[type(good)]) == 0:
        return good.base_price() * scalar
        #return statistics.mean(self.recent_prices[type(good)]) * scalar

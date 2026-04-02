
from enum import Enum


population_needs = [
    "Food",
    "Consumer Goods"
]


class PopulationType(Enum):
    UNEDUCATED = 1
    EDUCATED = 2
    HIGHLY_EDUCATED = 3
    EXPERT = 4


class Job(Enum):
    FARMER = 0
    SOLDIER = 1
    WORKER = 2
    ENGINEER = 3
    RESEARCHER = 4


class Good:
    def __init__(self, name, quantity, price, demand=0, recipe:list[str]=[]):
        self.name = name
        self.recipe = recipe
        self.quantity = quantity
        self.demand = demand
        self.price = price
        self.production_cost = 0
    
    def __add__(self, other):
        if self.name != other.name:
            raise ValueError("Cannot add goods of different types")
        return Good(self.name, self.quantity + other.quantity, self.price, self.demand)
    
    def __str__(self):
        return f"Good: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Demand: {self.demand}"

    def update_price(self):
        print("Base price:", self.price)
        print("Modifier:", self.demand / self.quantity if self.quantity > 0 else 1)
        self.price = self.price * (self.demand / self.quantity)


class Market:
    
    def __init__(self, market: list[Good]):
        self.market = market

    def __str__(self):
        return f"Market: {[good.name for good in self.market]}"

    def get_good_by_name(self, name):
        for good in self.market:
            if good.name == name:
                return good
        return None
    
    def update(self):
        for good in self.market:
            good.update_price()


class Population:

    def __init__(self, population, pop_type, job=None, wealth=0):
        self.population = population
        self.pop_type = pop_type
        self.job = job
        self.wealth = wealth
        self.purchase_orders = []
    
    def __str__(self):
        return f"Population: {self.population}, Type: {self.pop_type}, Job: {self.job}"
    
    def add_demand(self, market: Market):
        for good_name in population_needs:
            good = market.get_good_by_name(good_name)
            if good:
                good.demand += self.population
    
    def make_purchase_orders(self, market: Market):
        for good_name in population_needs:
            good = market.get_good_by_name(good_name)
            if good:
                print("Making purchase order for", min(self.population, self.wealth // good.price), "orders of", good_name, "at price", good.price)
                self.purchase_orders.append((good_name, min(self.population, self.wealth // good.price), good.price))


class People:
    def __init__(self, name, populations: list[Population]):
        self.name = name
        self.populations = populations

    def __str__(self):
        return f"People: {self.name}, Populations: {self.populations}"

    def sort(self):
        self.populations.sort(key=lambda x: x.wealth, reverse=True)
    
    def update_demand(self, market: Market):
        for population in self.populations:
            population.add_demand(market)
    
    def make_purchase_orders(self, market: Market):
        for population in self.populations:
            population.make_purchase_orders(market)
    
    def complete_purchase_orders(self, market: Market):
        for population in self.populations:
            for good_name, quantity, price in population.purchase_orders:
                good = market.get_good_by_name(good_name)
                if good:
                    print("Buying", quantity, good_name, "at price", price)
                    quantity_to_buy = min(quantity, good.quantity)
                    population.wealth -= quantity_to_buy * price
                    good.quantity -= quantity_to_buy
                    good.demand -= quantity_to_buy


class Company:
    def __init__(self, name, industries, capital):
        self.name = name
        self.industries = industries
        self.capital = capital
    
    def __str__(self):
        return f"Company: {self.name}, Industries: {[industry.name for industry in self.industries]}, Capital: {self.capital}"
    
    def update(self):
        for industry in self.industries:
            industry.update()


class Industry:

    def __init__(self, name, produced_good, required_goods, workforce, salary=0, capital=0):
        self.name = name
        self.produced_good = produced_good
        self.required_goods = required_goods
        self.workforce = workforce
        self.productivity = 3
        self.salary = salary
        self.capital = capital
    
    def __str__(self):
        return f"Industry: {self.name}, Produced Good: {self.produced_good.name}, Required Goods: {[good.name for good in self.required_goods]}, Workforce: {self.workforce}"

    def update(self):
        if len(self.required_goods) == 0:
            salary = self.salary * self.workforce.population
            if self.capital < salary:
                salary = self.capital
            self.produced_good.quantity += self.productivity * self.workforce.population
            self.capital += self.produced_good.price * self.produced_good.quantity
            self.workforce.wealth += salary
        else:
            pass


def process_sales(market: Market, people: list[People]):
    people.sort()
    for population in people:
        for good_name in population_needs:
            good = market.get_good_by_name(good_name)
            if good:
                quantity_to_buy = min(population.population, good.quantity)
                missing = 0
                if quantity_to_buy * good.price > population.wealth:
                    quantity_to_buy = population.wealth // good.price
                    missing = (population.population - quantity_to_buy) / population.population
                
                population.wealth -= quantity_to_buy * good.price
                good.quantity -= quantity_to_buy
                good.demand -= quantity_to_buy


from src.objects import *


if __name__ == "__main__":

    # Define some goods
    food = Good("Food", 100, 10)
    consumer_goods = Good("Consumer Goods", 50, 20)

    # Define market
    market = Market(market=[food, consumer_goods])

    # Define population
    population_farmer = Population(population=1000, pop_type=PopulationType.UNEDUCATED, job=Job.FARMER, wealth=10000)
    population_worker = Population(population=500, pop_type=PopulationType.EDUCATED, job=Job.WORKER, wealth=5000)
    people = People(name="People of Country", populations=[population_farmer, population_worker])

    # Define industries
    agriculture = Industry(name="Agriculture", produced_good=food, required_goods=[], workforce=population_farmer)
    manufacturing = Industry(name="Manufacturing", produced_good=consumer_goods, required_goods=[], workforce=population_worker)

    # Define company
    company = Company(name="AgriCorp", industries=[agriculture, manufacturing], capital=100000)



    # Print initial state
    for good in market.market:
        print(str(good))
    
    people.update_demand(market)

    company.update()

    people.make_purchase_orders(market)

    market.update()

    people.complete_purchase_orders(market)

    for good in market.market:
        print(str(good))
    

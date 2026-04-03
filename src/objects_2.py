
from enum import Enum
import math


class EducationLevel(Enum):
    CHILD = 0.5
    UNEDUCATED = 1
    EDUCATED = 2
    HIGHLY_EDUCATED = 3
    EXPERT = 4


class EducationType(Enum):
    BASIC_EDUCATION = 0
    ADVANCED_EDUCATION = 1
    RESEARCH = 2


class IndustryType(Enum):
    # Raw resources
    SUBSISTENCE = 0
    AGRICULTURE = 1
    MINING = 2
    # Civilian Manufacturing
    CONSUMER_GOODS = 3
    METALLURGY = 4
    VEHICLES = 5
    SHIPS = 6
    AIRCRAFT = 7
    SEMICONDUCTORS = 8
    CONSTRUCTION = 9
    # Military Manufacturing
    MILITARY_GOODS = 10
    AMMUNITION = 11
    # Services
    SERVICES = 12


class Good:
    def __init__(self, name:IndustryType, base_price:float):
        self.name = name
        self.price = base_price
        self.demand = 0
        self.quantity = 0
        self.production = 0


class Population:
    
    def __init__(self, number:int, education_level: EducationLevel):
        self.number = number
        self.employed = 0
        self.education_level = education_level
        self.required_goods = [
            (IndustryType.AGRICULTURE, 1),
            (IndustryType.CONSTRUCTION, 0.05),
        ]
        self.optional_goods = [
            (IndustryType.CONSUMER_GOODS, 0.5),
            (IndustryType.VEHICLES, 0.1),
            (IndustryType.SERVICES, 0.5)
        ]
    
    def kill(self, amount:int, industries:list):
        self.number = max(0, self.number - amount)
        if self.employed > self.number:
            # remove workers from industries
            industries.sort(key=lambda ind: ind.avg_salary, reverse=True)
            for industry in industries:
                if amount > 0:
                    amount = industry.kill_workers(amount, self.education_level)
            self.employed = self.number
    
    def promote_pops(self, majority_age:18, population:list):
        next_level = None
        for pop in population:
            if pop.education_level == EducationLevel.UNEDUCATED:
                next_level = pop
        if self.education_level == EducationLevel.CHILD:
            to_promote = self.number // majority_age
            self.number -= to_promote
            if next_level:
                next_level.number += to_promote


class Industry:
    
    def __init__(self, name:str, industry_type:IndustryType, base_productivity:float, technology_level:float, avg_salary:float, num_jobs:int, required_education: EducationLevel, average_production_value:float, input_goods:list[dict]=[]):
        self.name = name
        self.industry_type = industry_type
        self.base_productivity = base_productivity
        self.technology_level = technology_level
        self.avg_salary = avg_salary
        self.num_jobs = num_jobs
        self.employed = []
        self.total_hired = 0
        self.employment_rate = 0.0
        self.avg_production_value = average_production_value
        self.required_education = required_education
        self.avg_pop_education = 1.0
        self.productivity_bonuses = []
        self.productivity = self.calculate_productivity()
        self.input_goods = input_goods
        self.capital = 0
        self.stock = 0
        self.demand = 0
        self.demand_growth = 0
    
    def update_avg_pop_education(self):
        total_employed = 0
        for education_level, num_employed in self.employed:
            self.avg_pop_education += education_level.value * num_employed
            total_employed += num_employed
        if total_employed > 0:
            self.avg_pop_education /= total_employed
        else:
            self.avg_pop_education = 1.0
    
    def add_productivity_bonus(self, bonus: float):
        self.productivity_bonuses.append(bonus)
    
    def remove_productivity_bonus(self, bonus: float):
        if bonus in self.productivity_bonuses:
            self.productivity_bonuses.remove(bonus)
    
    def calculate_productivity(self) -> float:
        self.update_avg_pop_education()
        education_modifier = self.avg_pop_education / self.required_education.value
        if education_modifier > 1.0: education_modifier = math.cbrt(education_modifier)
        technology_modifier = 1.0 + (self.technology_level * 0.2)
        productivity = self.base_productivity * education_modifier * technology_modifier
        return productivity + productivity * sum(self.productivity_bonuses)

    def update_hiring(self, population:list[Population]):
        if self.total_hired < self.num_jobs:
            self.employment_rate = self.hire_best_employees(population)
        elif self.total_hired > self.num_jobs:
            self.employment_rate = self.fire_worst_employees(population)

    def hire_best_employees(self, population:list[Population]) -> float:
        population.sort(key=lambda pop: pop.education_level.value, reverse=True)
        for pop in population:
            if self.total_hired < self.num_jobs and pop.employed < pop.number:
                max_employable = min(pop.number - pop.employed, self.num_jobs - self.total_hired)
                to_hire = min(max_employable, self.num_jobs - self.total_hired)
                pop.employed += to_hire
                self.total_hired += to_hire
                self.employed.append((pop.education_level, to_hire))
        return self.total_hired / self.num_jobs
    
    def fire_worst_employees(self, population:list[Population]) -> float:
        if self.total_hired > self.num_jobs:
            for education_level, num_employed in sorted(self.employed, key=lambda x: x[0].value):
                to_fire = min(num_employed, self.total_hired - self.num_jobs)
                for pop in population:
                    if pop.education_level == education_level and pop.employed > 0:
                        max_fired = min(pop.employed, to_fire)
                        pop.employed -= max_fired
                        self.total_hired -= max_fired
                        self.employed.remove((education_level, num_employed))
                        if to_fire < num_employed:
                            self.employed.append((education_level, num_employed - max_fired))
                        break
        return self.total_hired / self.num_jobs
    
    def kill_workers(self, amount:int, education_level:EducationLevel) -> int:
        for education, employed in self.employed:
            if education == education_level:
                to_kill = min(employed, amount)
                amount = amount - to_kill
                new_employed = employed - to_kill
                self.total_hired -= to_kill
                self.employed.remove((education, employed))
                if new_employed > 0:
                    self.employed.append((education, new_employed))
        return amount
    
    def production(self) -> float:
        return self.calculate_productivity() * self.total_hired
    
    def _input_costs(self, industries:list) -> float:
        costs = 0.0
        for input_good in self.input_goods:
            for good_name, details in input_good.items():
                for industry in industries:
                    if industry.industry_type == good_name:
                        costs += details["quantity"] * industry.avg_production_value
        return costs
    
    def income(self) -> float:
        return self.production() * self.avg_production_value
    
    def expenses(self, industries:list) -> tuple[float, float]:
        salary = self.avg_salary * self.total_hired
        materials = self.production() * self._input_costs(industries)
        return salary, materials
    
    def gdp_contribution(self, industries:list) -> float:
        return self.income() - self.expenses(industries)[1]

    def profitability(self, industries:list) -> float:
        return self.income() - sum(self.expenses(industries))
    
    def optimise_production(self):
        productivity = self.calculate_productivity()
        change = 1.1 if self.demand > self.stock else 0.9
        required_jobs = (self.demand_growth * change) // productivity if productivity > 0 else self.num_jobs
        self.num_jobs = max(1, int(required_jobs))
    
    def calculate_optimal_salary(self, industries:list):
        budget = 0.8 * (self.income() - self._input_costs(industries) * self.production())
        optimal_salary = budget / self.num_jobs
        self.avg_salary = optimal_salary
    
    def buy_inputs(self, industries:list) -> float:
        production_multiplier = 1.0
        total_cost = 0.0
        purchase_percentages = []
        for input_good in self.input_goods:
            for good_name, details in input_good.items():
                for industry in industries:
                    if industry.industry_type == good_name:
                        percentage_cost = details["quantity"] * industry.avg_production_value
                        purchase_percentages.append(percentage_cost)
        for input_good in self.input_goods:
            for good, percentage in zip(input_good.items(), purchase_percentages):
                good_name, details = good
                required_quantity = details["quantity"] * self.production()
                for industry in industries:
                    if industry.industry_type == good_name:
                        resources_available =  min(required_quantity, industry.stock)
                        resource_budget = (percentage / sum(purchase_percentages)) if sum(purchase_percentages) > 0 else 1
                        max_purchasable = (self.capital * resource_budget) / industry.avg_production_value
                        resources_available = min(resources_available, max_purchasable)
                        if resources_available < required_quantity:
                            production_multiplier = min(production_multiplier, resources_available / required_quantity)
                        cost = resources_available * industry.avg_production_value
                        total_cost += cost
                        industry.stock -= min(required_quantity, industry.stock)
                        self.capital -= cost
        return production_multiplier
    
    def produce(self, industries:list):
        production = self.production()
        production_modifier = self.buy_inputs(industries)
        self.stock += production * production_modifier

    def sell(self):
        price_change = 0.0
        if self.demand != self.stock:
            price_change = 0.1 * (self.demand - self.stock) / self.demand if self.demand > 0 else 0
        to_sell = min(self.stock, self.demand)
        self.stock -= to_sell
        self.demand -= to_sell
        self.capital += to_sell * self.avg_production_value
        if price_change != 0.0:
            self.avg_production_value *= (1 + price_change)
    
    def update_demand(self, population:list[Population], industries:list) -> int:
        demand_growth = 0
        for pop in population:
            for good, quantity in pop.required_goods:
                if good == self.industry_type:
                    self.demand += pop.number * quantity
                    demand_growth += pop.number * quantity
            for good, quantity in pop.optional_goods:
                if good == self.industry_type:
                    self.demand += pop.number * quantity
                    demand_growth += pop.number * quantity
        for industry in industries:
            for input_good in industry.input_goods:
                for good_name, details in input_good.items():
                    if good_name == self.industry_type:
                        self.demand += industry.production() * details["quantity"]
                        demand_growth += industry.production() * details["quantity"]
        return demand_growth

    def update(self, population:list[Population], industries:list):
        self.demand_growth = self.update_demand(population, industries)
        self.produce(industries)
        self.sell()
        self.optimise_production()
        self.calculate_optimal_salary(industries)
        self.update_hiring(population)
    
    def __str__(self):
        return f"Industry: {self.name}\nType: {self.industry_type.name}\nTech Level: {self.technology_level}\nAvg Salary: {self.avg_salary}\nJobs: {self.num_jobs}\nEmployed: {self.total_hired}\nProductivity: {self.productivity:.2f}\nIncome: {self.income():.2f}"
    
    def print_self(self, industries:list):
        salary, material_costs = self.expenses(industries)
        print(f"Industry: {self.name}\nType: {self.industry_type.name}\nTech Level: {self.technology_level}\nAvg Salary: {self.avg_salary}\nJobs: {self.num_jobs}\nEmployed: {self.total_hired}\nProductivity: {self.productivity:.2f}\nIncome: {self.income():.2f}\nSalary Costs: {salary:.2f}\nMaterial Costs: {material_costs:.2f}\nProduction: {self.production():.2f}\nStock: {self.stock:.2f}\nDemand: {self.demand:.2f}\nCapital: {self.capital:.2f}")


class Nation:
    
    def __init__(self, name:str, population:list[Population], industries:list[Industry], growth_rate:float=3, mortality_rate:float=1, life_expectancy:float=50.0, age_of_majority:int=18):
        self.name = name
        self.population = population
        self.industries = industries
        self.growth_rate = growth_rate
        self.mortality_rate = mortality_rate
        self.life_expectancy = life_expectancy
        self.age_of_majority = age_of_majority

    def get_total_population(self) -> int:
        return sum(pop.number for pop in self.population)
    
    def get_total_jobs(self) -> int:
        return sum(ind.num_jobs for ind in self.industries)
    
    def get_total_employed(self) -> int:
        return sum(pop.employed for pop in self.population)
    
    def get_unemployment_rate(self) -> float:
        total_population = self.get_total_population()
        if total_population == 0:
            return 0.0
        return (total_population - self.get_total_employed()) / total_population
    
    def update_employment(self):
        for industry in self.industries:
            industry.update_hiring(self.population)

    def update_population(self):
        total_population = self.get_total_population()
        births = math.floor(total_population * (self.growth_rate / (2 * self.life_expectancy)))
        death_rate = self.mortality_rate / self.life_expectancy
        total_deaths = 0
        for pop in self.population:
            if pop.education_level == EducationLevel.CHILD:
                pop.number += births
                pop.promote_pops(self.age_of_majority, self.population)
            else:
                num_deaths = math.floor(pop.number * death_rate)
                total_deaths += num_deaths
                pop.kill(num_deaths, self.industries)
    
    def update_industries(self):
        self.industries.sort(key=lambda ind: ind.avg_salary, reverse=True)
        for industry in self.industries:
            industry.update(self.population, self.industries)
    
    def __str__(self):
        return f"Nation: {self.name}\nPopulation: {self.get_total_population()}\nUnemployment Rate: {self.get_unemployment_rate()*100:.2f}%\nIndustries:\n" + "\n".join([f"  {ind.name} (Jobs: {ind.num_jobs}, Employed: {ind.total_hired}, Productivity: {ind.calculate_productivity():.2f})" for ind in self.industries])



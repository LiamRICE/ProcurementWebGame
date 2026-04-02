
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
    # Agriculture
    SUBSISTENCE = 0
    AGRICULTURE = 1
    # Civilian Manufacturing
    CONSUMER_GOODS = 2
    METALLURGY = 3
    VEHICLES = 4
    SHIPS = 5
    AIRCRAFT = 6
    SEMICONDUCTORS = 7
    # Military Manufacturing
    MILITARY_GOODS = 8
    AMMUNITION = 9
    # Services
    SERVICES = 10


class Population:
    
    def __init__(self, number:int, education_level: EducationLevel):
        self.number = number
        self.employed = 0
        self.education_level = education_level
    
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


class Good:
    def __init__(self, name:IndustryType, base_price:float):
        self.name = name
        self.price = base_price
        self.demand = 0
        self.quantity = 0
        self.production = 0


class Market:

    def __init__(self, goods:list[Good]):
        self.market = goods
    



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
        productivity = self.base_productivity * education_modifier * technology_modifier * self.employment_rate
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
        return self.calculate_productivity() * self.num_jobs
    
    def _input_costs(self) -> float:
        costs = 0.0
        for input_good in self.input_goods:
            for good_name, details in input_good.items():
                costs += details["quantity"] * details["cost"]
        return costs
    
    def income(self) -> float:
        return self.production() * self.avg_production_value
    
    def expenses(self) -> tuple[float, float]:
        salary = self.avg_salary * self.total_hired
        materials = self.production() * self._input_costs()
        return salary, materials
    
    def gdp_contribution(self) -> float:
        return self.income() - self.expenses()[1]

    def profitability(self) -> float:
        return self.income() - sum(self.expenses())

    def optimise_production(self, market):
        pass
    
    def calculate_optimal_salary(self):
        budget = 0.8 * (self.income() - self._input_costs() * self.production())
        optimal_salary = budget / self.num_jobs
        self.avg_salary = optimal_salary
    
    def produce(self, market):
        production = self.production()
        for good in market.market:
            if good.name == self.industry_type:
                good.quantity += production
                good.production = production
                self.capital += self.income() - sum(self.expenses())

    def update(self, population:list[Population], market:Market):
        self.produce(market)
        self.optimise_production(market)
        self.calculate_optimal_salary()
        self.update_hiring(population)
    
    def __str__(self):
        return f"Industry: {self.name}\nType: {self.industry_type.name}\nTech Level: {self.technology_level}\nAvg Salary: {self.avg_salary}\nJobs: {self.num_jobs}\nEmployed: {self.total_hired}\nProductivity: {self.calculate_productivity():.2f}\nIncome: {self.income():.2f}\nExpenses: {self.expenses()[0]:.2f} (Salary), {self.expenses()[1]:.2f} (Materials)\nProfitability: {self.profitability():.2f}"


class Nation:
    
    def __init__(self, name:str, population:list[Population], industries:list[Industry], market:Market, growth_rate:float=3, mortality_rate:float=1, life_expectancy:float=50.0, age_of_majority:int=18):
        self.name = name
        self.population = population
        self.industries = industries
        self.market = market
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
    
    def update_employement(self):
        self.industries.sort(key=lambda ind: ind.avg_salary, reverse=True)
        for industry in self.industries:
            industry.update_hiring(self.population)
    
    def update_population(self):
        total_population = self.get_total_population()
        births = total_population * (self.growth_rate / (2 * self.life_expectancy))
        death_rate = self.mortality_rate / self.life_expectancy
        total_deaths = 0
        for pop in self.population:
            if pop.education_level == EducationLevel.CHILD:
                pop.number += births
                pop.promote_pops(self.age_of_majority, self.population)
            else:
                num_deaths = pop.number * death_rate
                total_deaths += num_deaths
                pop.kill(num_deaths, self.industries)
                
    def __str__(self):
        return f"Nation: {self.name}\nPopulation: {self.get_total_population()}\nUnemployment Rate: {self.get_unemployment_rate()*100:.2f}%\nIndustries:\n" + "\n".join([f"  {ind.name} (Jobs: {ind.num_jobs}, Employed: {ind.total_hired}, Productivity: {ind.calculate_productivity():.2f})" for ind in self.industries])



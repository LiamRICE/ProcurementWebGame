# from src.objects import *
from src.objects_2 import *


if __name__ == "__main__":

    # Populations
    pop0 = Population(200, EducationLevel.CHILD)
    pop1 = Population(800, EducationLevel.UNEDUCATED)
    pop2 = Population(500, EducationLevel.EDUCATED)
    pop3 = Population(200, EducationLevel.HIGHLY_EDUCATED)

    # Industries
    industry1 = Industry(
        "Agriculture",
        IndustryType.AGRICULTURE,
        base_productivity=25,
        technology_level=1,
        avg_salary=150,
        num_jobs=1000,
        required_education=EducationLevel.UNEDUCATED,
        average_production_value=6.0,
        input_goods=[]
    )
    industry2 = Industry(
        "Manufacturing",
        IndustryType.CONSUMER_GOODS,
        base_productivity=10,
        technology_level=1,
        avg_salary=200,
        num_jobs=500,
        required_education=EducationLevel.UNEDUCATED,
        average_production_value=30.0,
        input_goods=[
            {"One": {
                "quantity": 1,
                "cost": 12.0
            }}
        ]
    )
    industry3 = Industry(
        "Vehicles",
        IndustryType.VEHICLES,
        base_productivity=0.2,
        technology_level=1,
        avg_salary=300,
        num_jobs=200,
        required_education=EducationLevel.EDUCATED,
        average_production_value=2000.0,
        input_goods=[
            {"One": {
                "quantity": 1,
                "cost": 250.0
            }},
            {"Two": {
                "quantity": 0.2,
                "cost": 800.0
            }}
        ]
    )

    # Market
    good1 = Good(IndustryType.AGRICULTURE, base_price=6.0)
    good2 = Good(IndustryType.CONSUMER_GOODS, base_price=30.0)
    good3 = Good(IndustryType.VEHICLES, base_price=2000.0)
    market = Market([good1, good2, good3])

    # Nation
    nation = Nation("Testland", [pop0, pop1, pop2, pop3], [industry1, industry2, industry3], market)


    #=== TEST ===#
    print("===== INITIAL STATE =====")
    print(nation)

    print("\n===== AFTER UPDATING EMPLOYMENT =====")
    nation.update_employement()
    print(nation)

    print("\n===== AFTER UPDATING INDUSTRIES =====")
    for ind in nation.industries:
        print("\n"+str(ind))

    print("\n===== AFTER UPDATING POPULATION =====")
    nation.update_population()
    print(nation)

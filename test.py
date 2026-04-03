# from src.objects import *
from src.objects_2 import *


if __name__ == "__main__":

    # Populations
    pop0 = Population(300, EducationLevel.CHILD)
    pop1 = Population(1800, EducationLevel.UNEDUCATED)
    pop2 = Population(1000, EducationLevel.EDUCATED)
    pop3 = Population(500, EducationLevel.HIGHLY_EDUCATED)

    # Industries
    industry1 = Industry(
        "Agriculture",
        IndustryType.AGRICULTURE,
        base_productivity=50,
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
        base_productivity=50,
        technology_level=1,
        avg_salary=200,
        num_jobs=500,
        required_education=EducationLevel.UNEDUCATED,
        average_production_value=30.0,
        input_goods=[
            {IndustryType.AGRICULTURE: {
                "quantity": 2,
            }}
        ]
    )
    industryX = Industry(
        "Metallurgy",
        IndustryType.METALLURGY,
        base_productivity=20,
        technology_level=1,
        avg_salary=200,
        num_jobs=300,
        required_education=EducationLevel.UNEDUCATED,
        average_production_value=3.0,
        input_goods=[]
    )
    industryY = Industry(
        "Services",
        IndustryType.SERVICES,
        base_productivity=10,
        technology_level=1,
        avg_salary=500,
        num_jobs=400,
        required_education=EducationLevel.EDUCATED,
        average_production_value=200.0,
        input_goods=[]
    )
    industry3 = Industry(
        "Vehicles",
        IndustryType.VEHICLES,
        base_productivity=1,
        technology_level=1,
        avg_salary=300,
        num_jobs=200,
        required_education=EducationLevel.EDUCATED,
        average_production_value=2000.0,
        input_goods=[
            {IndustryType.METALLURGY: {
                "quantity": 25,
            }},
            {IndustryType.SERVICES: {
                "quantity": 3,
            }}
        ]
    )

    # Nation
    nation = Nation("Testland", [pop0, pop1, pop2, pop3], [industry1, industry2, industry3, industryY, industryX])


    #=== TEST ===#
    print("===== INITIAL STATE =====")
    print(nation)
    nation.update_employment() # initial employment state

    for i in range(100):
        print(f"\n===== UPDATE CYCLE {i+1} =====")

        print("\n===== AFTER UPDATING EMPLOYMENT =====")
        nation.update_industries()
        print(nation)

        print("\n===== AFTER UPDATING INDUSTRIES =====")
        for ind in nation.industries:
            print("")
            ind.print_self(nation.industries)

        print("\n===== AFTER UPDATING POPULATION =====")
        nation.update_population()
        print(nation)

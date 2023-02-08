import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv", sep = ",")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    average_age_men = df[df["sex"] == "Male"]["age"].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df[df["education"] == "Bachelors"]["education"].count() * 100 / len(df)).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education earn less than or equal to 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[((df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate"))]["salary"].count()
    
    lower_education = df[(df["education"] != "Bachelors") & (df["education"] != "Masters") & (df["education"] != "Doctorate")]["education"].count()

    # percentage with salary >50K
    higher_education_rich = ((df[((df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")) & (df["salary"] == ">50K")]["salary"].count() * 100) / higher_education).round(1)
    
    lower_education_rich = ((df[(df["education"] != "Bachelors") & (df["education"] != "Masters") & (df["education"] != "Doctorate") & (df["salary"] == ">50K")]["salary"].count() * 100) / lower_education).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df[(df["hours-per-week"] == min_work_hours)]["salary"].count()

    rich_percentage = ((df[(df["hours-per-week"] == min_work_hours) & (df["salary"] == ">50K")]["salary"].count() * 100 ) / num_min_workers).round(1)

    # What country has the highest percentage of people that earn >50K?
    df_people_country = pd.DataFrame(df.groupby(["native-country"]).size())
    df_people_country.rename(columns = {0: "number_people"}, inplace = True)
    df_people_country_salary = pd.DataFrame(df.groupby(["native-country","salary"],as_index=False).size())
    df_people_country_salary.rename(columns = {"size": "number_people"}, inplace = True)
    df_people_country_pivot= df_people_country_salary.pivot(index ='native-country', columns ='salary', values= ["number_people"])
    df_people_country_pivot.columns = df_people_country_pivot.columns.droplevel(0)

    highest_earning_country =  pd.DataFrame(df_people_country_pivot[">50K"] * (100 / df_people_country["number_people"]), columns= [">50K"])[">50K"].idxmax()
    
    highest_earning_country_percentage = pd.DataFrame(df_people_country_pivot[">50K"] * (100 / df_people_country["number_people"]), columns= [">50K"])[">50K"].max().round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df["salary"] == ">50K") & (df["native-country"] == "India")].groupby(["occupation"]).size().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

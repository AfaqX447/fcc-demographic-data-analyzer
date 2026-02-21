import pandas as pd

def calculate_demographic_data(print_data=True):
    # 1. Load the data
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
    ]
    
    # We use header=None because your file starts with data immediately
    df = pd.read_csv('adult.data.csv', names=column_names, header=0)

    # --- ADD THE VERIFICATION LINE HERE ---
    print(f"Total rows loaded: {len(df)}") 
    # --------------------------------------

    # 🛠️ THE NEW FIX: Remove the trailing blank line
    df = df.dropna()

    # 2. Clean whitespace from all text columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # 3. 🔥 FORCE NUMERIC (This fixes your TypeError)
    # This converts the 'age' column from strings to actual integers
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['hours-per-week'] = pd.to_numeric(df['hours-per-week'], errors='coerce')

    # --- Analysis Logic ---
    
    # Race count
    race_count = df['race'].value_counts()

    # Average age of men (Now .mean() will work!)
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # Percentage with Bachelors
    percentage_bachelors = round((df['education'] == 'Bachelors').sum() / len(df) * 100, 1)

    # Higher/Lower Education
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]

    # Percentage earning >50K
    higher_education_rich = round((higher_education['salary'] == '>50K').sum() / len(higher_education) * 100, 1)
    lower_education_rich = round((lower_education['salary'] == '>50K').sum() / len(lower_education) * 100, 1)

    # Min hours and rich percentage
    min_work_hours = df['hours-per-week'].min()
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((num_min_workers['salary'] == '>50K').sum() / len(num_min_workers) * 100, 1)

    # Country analysis
    country_stats = df.groupby('native-country')['salary'].apply(lambda x: (x == '>50K').sum() / len(x) * 100)
    highest_earning_country = country_stats.idxmax()
    highest_earning_country_percentage = round(country_stats.max(), 1)

    # India occupation
    top_IN_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation'].value_counts().idxmax()

    if print_data:
        print("Average age of men:", average_age_men)
        # ... (you can add other prints here to see them in terminal)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
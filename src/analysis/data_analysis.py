import pandas as pd

def analyze_data():
    schools_df = pd.read_csv('data/school_data.csv')
    housing_df = pd.read_csv('data/housing_data.csv')
    
    # Sort schools by performance (ascending) and select bottom 25%
    worst_schools = schools_df.sort_values('performance').head(len(schools_df) // 4)
    
    # Match housing data with worst-performing school districts
    # This is a simplified example - you'd need to implement logic to match houses to school districts
    worst_district_housing = housing_df[housing_df['zip_code'].isin(worst_schools['zip_code'])]
    
    return worst_district_housing

if __name__ == "__main__":
    results = analyze_data()
    print(results)
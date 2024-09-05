from scraper.school_scraper import scrape_disd_high_schools
from scraper.housing_scraper import scrape_housing_data
from analysis.data_analysis import analyze_data

def main():
    # Scrape school data
    school_data = scrape_disd_high_schools()
    
    # Get relevant zip codes from school data
    zip_codes = school_data['zip_code'].unique().tolist()
    
    # Scrape housing data
    housing_data = scrape_housing_data(zip_codes)
    
    # Analyze data
    results = analyze_data()
    
    # Output results (you could save to a file, display in a web app, etc.)
    print(results)

if __name__ == "__main__":
    main()
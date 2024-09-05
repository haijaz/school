import os
from scraper.school_scraper import process_or_download_pdfs
from analysis.data_analysis import analyze_data

def main():
    # Create 'data' directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # Process local PDF files or download if not available
    pdf_directory = 'C:\\dev\\school\\src\\data'
    school_data = process_or_download_pdfs(pdf_directory)
    
    if not school_data.empty:
        # Analyze data
        results = analyze_data()
        
        # Output results (you could save to a file, display in a web app, etc.)
        print(results)
    else:
        print("Error: No school data available. Cannot proceed with analysis.")

if __name__ == "__main__":
    main()
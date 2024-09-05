import os
import pandas as pd
import re
import PyPDF2
import requests
from bs4 import BeautifulSoup

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def extract_data_from_pdf(filename):
    school_data = {}
    
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    # Extract school name
    name_match = re.search(r'School Name:\s*(.*?)\n', text)
    if name_match:
        school_data['name'] = name_match.group(1)
    
    # Extract performance score
    performance_match = re.search(r'Overall Score:\s*(\d+)', text)
    if performance_match:
        school_data['performance'] = performance_match.group(1)
    
    # Check if the school has 8th, 9th, 10th, 11th, or 12th grade
    grade_pattern = r'Grade (?:8|9|10|11|12):\s*\d+'
    if re.search(grade_pattern, text):
        school_data['has_target_grades'] = True
    else:
        school_data['has_target_grades'] = False
    
    print(f"Extracted data: {school_data}")
    return school_data if school_data else None

def process_or_download_pdfs(pdf_directory):
    schools = []
    
    # Always check the website for PDFs
    url = "https://mydata.dallasisd.org/SL/SD/cdp.jsp"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pdf_links = soup.find_all('a', href=re.compile(r'.*\.pdf$'))
    
    os.makedirs(pdf_directory, exist_ok=True)
    
    for link in pdf_links:
        pdf_url = 'https://mydata.dallasisd.org' + link['href']
        pdf_filename = os.path.join(pdf_directory, os.path.basename(pdf_url))
        
        # Check if the file already exists
        if not os.path.exists(pdf_filename):
            print(f"Downloading: {pdf_url}")
            download_pdf(pdf_url, pdf_filename)
        else:
            print(f"File already exists: {pdf_filename}")
        
        print(f"Processing: {pdf_filename}")
        school_data = extract_data_from_pdf(pdf_filename)
        if school_data and school_data['has_target_grades']:
            schools.append(school_data)
    
    print(f"Total schools with target grades processed: {len(schools)}")
    
    df = pd.DataFrame(schools)
    df = df.drop(columns=['has_target_grades'])  # Remove the temporary column
    print("DataFrame columns:", df.columns)
    print("DataFrame head:\n", df.head())
    
    df.to_csv('data/school_data.csv', index=False)
    return df

if __name__ == "__main__":
    pdf_directory = 'C:\\dev\\school\\src\\data'
    process_or_download_pdfs(pdf_directory)
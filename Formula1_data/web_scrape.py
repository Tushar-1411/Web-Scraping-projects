from bs4 import BeautifulSoup
from pip._vendor import requests
import csv

# Website-url : 

events = ['races','fastest-laps','drivers']

def get_details(file_obj, event):
    writer = csv.writer(file_obj)
    years = list(range(1950,2023))
    record = 1
    
    for year in years:
        # Make a request to the website
        url = f"https://www.formula1.com/en/results.html/{year}/{event}.html"
        page = requests.get(url)
        page = page.content

        # Parse the HTML content of the page
        soup = BeautifulSoup(page, "lxml")

        # Obtain the table 
        table = soup.find('div', class_ = 'table-wrap')

        # To extract the headers of the table
        headers = table.table.thead.tr.find_all('th')
        headers = [title.text for title in headers if title.text != ""]

        # This section makes sure that we write the header only once 
        # Or you can manually write the headers in the csv file
        if (record == 1):
            writer.writerow(headers + ['year'])
        record += 1
            
        # table-contents extracts all the rows from the table
        table_contents = table.find('tbody')
        for rows in table_contents.find_all('tr'):
            details = [tags.text for tags in  rows.find_all('td') if tags.text != ""]
            details = [x.replace('\n',' ').strip() for x in details]
            writer.writerow(details + [year])
    

for event in events:
    file_name = f'GrandPrix_{event}_details_1950_to_2022.csv'
    with open(file_name,'w') as f:
        get_details(f, event)
        
    



   




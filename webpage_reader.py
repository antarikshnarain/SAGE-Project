import requests as rq
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil.parser import parse
import pytz
"""
table.wikitable collapsible mw-collapsible mw-made-collapsible

table1:
    start: 4

"""

class PageReader:
    def __init__(self, page_url):
        """
        params page_url : string url of page
        """
        self.url = page_url
    
    def parse_page(self):
        response = rq.get(self.url)
        soup = bs(response.text,'html5lib')
        tables = soup.find_all('table', class_='wikitable')
        # Send Table 1 for Orbital Satellite data
        self.extract_data(tables[0])

    
    def extract_data(self, table_data):
        """
        Function responsible for extracting data from the website
        """
        table_rows = table_data.find_all('tr')
        for i in range(4,len(table_rows)):
            row_data = table_rows[i].find_all('td')
            if len(row_data) == 5:
                # Extract Date
                rec_date = self.clean_data_date(row_data[0].getText())
                print("---------------------------------")
                print(rec_date, end='\t')
            elif len(row_data) == 4:
                # Previous date to be used
                pass
            elif len(row_data) == 6:
                # Satellite info for rec_date
                rec_flight_status = self.clean_data(row_data[5].text)
                print(rec_flight_status, end='\t')
    
    def clean_data(self, text):
        expressions = [
            r"<br>",
            r"<sub+"
        ]
        for expression in expressions:
            text = re.sub(expression, "", text)

        return text
    
    def clean_data_date(self, date):
        date = re.sub(r"[^ \w\d:].*","",date)
        #date = datetime.strptime(date,'%d %B%H:%M')
        date = parse(date)
        date = date.replace(year=2019)
        date = pytz.utc.localize(date)
        return date.isoformat()

import requests as rq
import re
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
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
        records = self.extract_data(tables[0])
        # Create records date wise
        #date = pytz.utc.localize(date)
        present_date = pytz.utc.localize(parse("2019-01-01"))
        count = 0
        for rec in records:
            while present_date < rec[0]:
                print ("%s,%d"%(present_date.isoformat(),count))
                present_date = present_date + timedelta(days=1)
                count = 0
            if present_date == rec[0]:
                count += 1
        
        print ("%s,%d"%(present_date.isoformat(),count))
        present_date = present_date + timedelta(days=1)

        # Print for remaining days
        while present_date <= pytz.utc.localize(parse("2019-12-31")):
            print ("%s,%d"%(present_date.isoformat(),0))
            present_date = present_date + timedelta(days=1)

    
    def extract_data(self, table_data):
        """
        Function responsible for extracting data from the website
        """
        table_rows = table_data.find_all('tr')
        was_success = False
        rec_date = None
        records = []
        for i in range(4,len(table_rows)):
            row_data = table_rows[i].find_all('td')
            if len(row_data) == 5:
                # Add record if successful
                if rec_date != None and was_success:
                    records.append((rec_date, was_success))
                # Extract Date
                rec_date = self.clean_data_date(row_data[0].getText())
                was_success = False
                #print("---------------------------------")
                #print(rec_date, end='\t')
            elif len(row_data) == 4:
                # Previous date to be used
                pass
            elif len(row_data) == 6:
                # Satellite info for rec_date
                rec_flight_status = self.clean_data(row_data[5].text).lower()
                if rec_flight_status in ["operational", "en route", "successful"]:
                    # Can be changed for count
                    was_success = True
        
        if rec_date != None and was_success:
            records.append((rec_date, was_success))
        return records
    
    def clean_data(self, text):
        expressions = [
            r"<br>",
            r"<sub+",
            r"[^ \w]"
        ]
        for expression in expressions:
            text = re.sub(expression, "", text)

        return text
    
    def clean_data_date(self, date):
        date = re.sub(r"[^ \w\d:].*","",date)
        #date = datetime.strptime(date,'%d %B%H:%M')
        date = parse(date)
        # Loosing Time data
        date = date.replace(year=2019,hour=0,minute=0,second=0,microsecond=0)
        date = pytz.utc.localize(date)
        return date

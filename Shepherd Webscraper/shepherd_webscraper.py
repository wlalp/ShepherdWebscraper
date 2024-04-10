'''Contains ShepherdScraper class and a main method
    Author: William Pugh
    CIS 321 Webscraper project
'''
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests

class ShepherdScraper():
    '''This class scrapes the staff website of a given department at Shepherd University for staff information'''
    def __init__(self,department=None):
        '''Initializes scraper with a given department, if no department is provided the program will close'''
        self._dep = department
        url = f"https://www.shepherd.edu/{department}/staff/"
        req = requests.get(url,timeout=5.0)
        response = requests.head(url,timeout=5.0)
        if response.status_code != 200 or self._dep is None:
            print("Error: The given department either does not exist, or was input incorrectly. Please restart the program and try again.")
            sys.exit()
        soup = BeautifulSoup(req.text, "html.parser")

        self.staff = soup.find_all("div",{"class":"inner"})
        self.staff.pop(0)
        self.names= self.get_names()

    def name_processor(self,name):
        '''Removes suffixes such as Ph.D or M.S. from staff names'''
        if name is None:
            return None
        name = name.text.strip().split(",")
        proc = name[0]
        return proc

    def get_members(self):
        '''Returns a list of the members as well as the listed information associated with them on their staff site'''
        staff_mems =[]
        for staff_mem in self.staff:
            member = {}
            rows = staff_mem.find_all("tr")
            for row in rows:
                column = row.find("th")
                if column is not None:
                    if column.text.strip() in self.names:
                        member["Name"] = column.text.strip()
                        continue
                    field = row.find("td")
                    key = column.text.strip()
                    if key == "Email":
                        value = field.text.strip()
                        split = value.split("\t")
                        value = split[0]
                    else:
                        if field is not None:
                            value = field.text.strip()
                        else:
                            value = None
                    member[key] = value

            staff_mems.append(member)
        return staff_mems

    def get_names(self):
        '''Retrieves the name of the staff members from the staff soup'''
        return [self.name_processor(s.find("h2")) for s in self.staff if s.find("h2") is not None]

    def clean_data(self):
        '''Restructures the data into a dictionary with the keys Name, Email, Phone, and Office'''
        cleaned = []
        name_index = 0
        for mem in self.get_members():
            member = {"Name":None,"Title":None,"Email":None,"Phone":None,"Office":None}
            for key, value in mem.items():
                if key in member:
                    member[key] = value
            if member["Name"] is None:
                member["Name"] = self.names[name_index]
            name_index += 1
            cleaned.append(member)

        return cleaned

    def create_frame(self):
        '''Initializes a dataframe from the structured data'''
        staff_frame = pd.DataFrame(self.clean_data())
        return staff_frame

    def print_frame(self):
        '''Prints the dataframe'''
        print("Preview of the output CSV file:\n")
        print(self.create_frame())

    def create_csv(self):
        '''Creates a csv containing the data in the dataframe'''
        filename = f"shep_{self._dep}_staffinfo.csv"
        frame = self.create_frame()
        frame.to_csv(filename)
        print(f"CSV file: {filename} created!")

def main():
    '''Main method queries user for a department and generates output accordingly'''
    dep = input("Please input the desired department.\n")
    scraper = ShepherdScraper(dep)
    scraper.print_frame()
    scraper.create_csv()

if __name__ == "__main__":
    main()

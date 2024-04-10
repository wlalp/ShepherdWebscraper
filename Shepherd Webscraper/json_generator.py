'''Contains the JsonGen class and a demonstration of its functionality'''
import csv
import json

class JsonGen():
    '''Generates a JSON file from a csv file'''
    def __init__(self,csv_file,json_filename = None):
        self.filename = csv_file

        if json_filename is None:
            self.j_filename = self.filename.removesuffix(".csv") + ".json"
        else:
            if json_filename.endswith(".json"):
                self.j_filename = json_filename
            else:
                self.j_filename = json_filename + ".json"

        self.j_text = ''
    def csv_to_dicts(self):
        '''Reads in the csv file as a list of dicts'''
        dicts = []
        try:
            with open(self.filename,"r",encoding='utf-8') as fn:
                reader = csv.DictReader(fn)
                for row in reader:
                    dicts.append(row)
        except FileNotFoundError:
            print("The given csv file was invalid.")
        return dicts

    def clean_data(self):
        '''Removes null or blank fields from the created dictionaries'''
        dicts = self.csv_to_dicts()
        cleaned = []

        for d in dicts:
            remove_ks = set()
            for k, v in d.items():
                if v is None or v == '':
                    remove_ks.add(k)
            cleaned.append({k:v for k,v in d.items() if k not in remove_ks})
        return cleaned

    def write_json(self):
        '''Writes the cleaned data to the JSON file'''
        ret_j = json.dumps(self.clean_data(),indent= 2,ensure_ascii=False)

        with open(self.j_filename,"w",encoding='utf-8') as jf:
            jf.write(ret_j)
        self.j_text = ret_j

def demo():
    '''Demonstrates the functionality of JsonGen using an example csv file'''
    demo_file = "shep_cme_staffinfo.csv"
    print(f"Reading from {demo_file}...")
    j_gen = JsonGen(demo_file)
    j_gen.write_json()
    print(f"{j_gen.j_filename} created!")
    print("The following is a preview of the output JSON file.\n")
    print(j_gen.j_text[0:500] +"\n...")

if __name__ == "__main__":
    demo()

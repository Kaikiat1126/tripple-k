import csv
import random
from ..app.country import countries

def clean_csv(file_path):
    csv_file = open(file_path, 'r')
    reader = csv.DictReader(csv_file)
    data = []
    for row in reader:
        # replace the \n with space 
        for key in row.keys():
            row[key] = row[key].replace('\n', ' ')
        #randomly assign the country
        row["Customer Location"] = random.choice(list(countries.keys()))
        # uppercase for the device used column first letter
        row["Device Used"] = row["Device Used"].capitalize()
        row["Payment Method"] = row["Payment Method"].capitalize()

        #if the customer age is less than 18, no need to include it
        if int(row['Customer Age']) < 18:
            continue
        else:
            data.append(row)
    csv_file.close()

    with open(file_path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data[0].keys())
        for row in data:
            csv_writer.writerow(row.values())
            

clean_csv('backend\dataset\Fraudulent_E-Commerce_Transaction_Data.csv')
    

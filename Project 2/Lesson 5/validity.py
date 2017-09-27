"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for i in range(3):
            reader.next()
            
        valid_data = []
        invalid_data = []
        for row in reader:
            try:
                year = int(row['productionStartYear'][:4])
            except:
                year = None
            
            if (year >= 1886 and year <= 2014):
                row['productionStartYear'] = str(year)
                valid_data.append(row)
            else:
                invalid_data.append(row)

    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "w") as vld:
        writer = csv.DictWriter(vld, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in valid_data:
            writer.writerow(row)

    with open(output_bad, "w") as invld:
        writer = csv.DictWriter(invld, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in invalid_data:
            writer.writerow(row)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()

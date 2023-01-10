#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.

"""
import codecs
import csv
import json
import pprint
import codecs
import re
from sets import Set

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    # initiate the field types as empty sets
    for field in fields:
        #The field types as set
        fieldtypes[field] = set([])
        
    with open(CITIES) as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames # column put into header
         
        for i, row in enumerate(reader):
            #Skipping  row 1 to 4
            if (i < 4) :
                continue
            for key in fields:
                val = row[key]
                # For Empty strings in row 
                if (val == "" or val == "NULL") :
                    fieldtypes[key].update([type(None)]) 
                    continue
                # For List type in row
                if (re.match('{', val)) : 
                    fieldtypes[key].update([type([])])
                    continue
                # Int type in row
                try:
                    val = int(val)
                    fieldtypes[key].update([type(1)])
                    continue
                except ValueError:  
                    ignore = 1
                #Float type in row
                try:
                    val = float(val)
                    fieldtypes[key].update([type(1.1)])
                    continue
                # for string (str) type
                except ValueError:  
                    ignore = 1 
                print "String: ", key, val
                fieldtypes[key].update([type('b')])
        
    return fieldtypes

def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()

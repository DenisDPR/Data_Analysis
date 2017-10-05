import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus
import schema

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from num2words import num2words

OSMFILE = "DAR.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

num_line_street_re = re.compile(r'\d0?(st|nd|rd|th|)\s(Line)$', re.IGNORECASE) # Spell lines ten and under
nth_re = re.compile(r'\d\d?(st|nd|rd|th|)', re.IGNORECASE)
nesw_re = re.compile(r'\s(North|East|South|West)$')

expected_street_types = ["Street",
            "Avenue",
            "Drive",
            "Court",
            "Place",
            "Lane",
            "Road",
            "Trail",
            "Parkway",
            "Gate",
            "Terrace",
            "Way"]

mapping = {
            "St": "Street",
            "St.": "Street",
            "STREET": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Rd": "Road",
            "Rd.": "Road",
            "Trl": "Trail",
            "Ct": "Court",
            "Ct.": "Court",
            "Crt": "Court",
            "Crt.": "Court",
            "N.": "North",
            "N": "North",
            "E.": "East",
            "E": "East",
            "S.": "South",
            "S": "South",
            "W.": "West",
            "W": "West"
          }

street_mapping = {
                   "St": "Street",
                   "St.": "Street",
                   "ST": "Street",
                   "STREET": "Street",
                   "Ave": "Avenue",
                   "Ave.": "Avenue",
                   "Rd.": "Road",
                   "Dr.": "Drive",
                   "Dr": "Drive",
                   "Rd": "Road",
                   "Rd.": "Road",
                   "Cir": "Circle",
                   "Cir.": "Circle",

                }
# For streets with number such as 1st, 2nd etc
lane_mapping = {
                     "1st": "First",
                     "2nd": "Second",
                     "3rd": "Third",
                     "4th": "Fourth",
                     "5th": "Fifth",
                     "6th": "Sixth",
                     "7th": "Seventh",
                     "8th": "Eighth",
                     "9th": "Ninth",
                     "10th": "Tenth"
                   }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street_types:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name):
    """
    For consistency, accuracy data is cleaned to be
    used in SQL database
    """
    if num_line_street_re.match(name):
        nth = nth_re.search(name)
        name = lane_mapping[nth.group(0)] + " Line"
        return name

    elif name == "Ahmed & Mohamed Line" or name == "Ahmed/Mohamed Line":
        name = "Ahmed-Mohamed Line"
        return name

    else:
        original_name = name
        for key in mapping.keys():
            # When mapping key match such as "St." 
            type_fix_name = re.sub(r'\s' + re.escape(key) + r'$', ' ' + mapping[key], original_name)
            nesw = nesw_re.search(type_fix_name)
            if nesw is not None:
                for key in street_mapping.keys():
                    # No renaming proper names.
                    dir_fix_name = re.sub(r'\s' + re.escape(key) + re.escape(nesw.group(0)), " " + street_mapping[key] + nesw.group(0), type_fix_name)
                    if dir_fix_name != type_fix_name:
                        return dir_fix_name
            if type_fix_name != original_name:
                return type_fix_name
    # Check for capitalized names such as street
    last_word = original_name.rsplit(None, 1)[-1]
    if last_word.islower():
        original_name = re.sub(last_word, last_word.title(), original_name)
    return original_name

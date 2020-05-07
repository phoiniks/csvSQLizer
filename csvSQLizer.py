#!/usr/bin/python
#-*- coding: utf-8 -*-
# andreas@grellopolis.de, 2014
# I wrote this tiny Python script for security reasons: Instead of delivering corrupt or otherwise incorrect CSV data for our MySQL db, I prefer testing.
# And as I didn't find sqlite3 installed on our server, I decided to use Python, because it comes with sqlite3 included, thus providing
# a means to do the aforementioned SQL/CSV testing. As long as this script doesn't produce any error messages and you can see reasonable output,
# your CSV data should be ok. Caveat: Of course, this script doesn't handle huge amounts of data as efficiently as MySQL does. 
# It's just for testing, if some piece of data fits into the fields prescribed by some header line.

import sqlite3
import re
import sys
from string import strip
from os import getcwd

con = sqlite3.connect("%s.db" %getcwd().split("/")[-1])

try:
    sys.argv[1] != ""
except:
    print("\nPlease provide a commandline parameter like so: ./csvSQLizer.py xxx.csv\n")
    exit(-1)


CSV = open(sys.argv[1]).readlines()

fields = CSV[0].split("|")

def gen(lst):
    for l in lst:
        if re.match("[0-9]", l):     # This would have to be changed when working with other data than PANAGON, KOVIS or EASY sheets.
            l = sys.argv[1][0] + l
            l = l.strip("\n")
            yield l
        else:
            l = l.strip("\n")
            yield l


fields = list(gen(fields))

partial = " text, ".join(fields) + " text"

sql = "CREATE TABLE IF NOT EXISTS mapping(" + partial + ")"

cur = con.cursor()

cur.execute(sql)

sql = "INSERT INTO mapping (%s) values(" %(", ".join(fields))

sql += "?, " * len(fields)
sql = re.sub("\,\s*$", ")", sql)

for C in CSV[:]:
    lst = C.split("|")
    lst = [l.strip().decode("utf-8") for l in lst]
    cur.execute(sql, lst)

con.commit()

sql = "SELECT * FROM mapping"

cur.execute(sql)

lst = cur.fetchall()

for l in lst:
    for e in l:
        print(e + "|"),
    print("\n\n");

con.close()

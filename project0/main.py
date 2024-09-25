# -*- coding: utf-8 -*-
# Example main.py
import argparse
import requests
import PyPDF2
import re
import sqlite3
import pandas as pd
import os

def main(url):
    # Download data
    fetchincidents(url)
    incidents = extractincidents()
    #db = createdb()
    #populatedb(db, incidents)	
    # Print incident counts
    #status(db)

def fetchincidents(url):
    response = requests.get(url)
    with open("./resources/data.pdf","wb") as file:
        file.write(response.content)

def createdb():
    if os.path.exists("./resources/normanpd.db"):
        os.remove("./resources/normanpd.db")
    con = sqlite3.connect("./resources/normanpd.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT)")
    con.commit()
    return con

def extractincidents():
    data = []
    with open("./resources/data.pdf","rb") as file:
        reader = PyPDF2.PdfReader(file)
        pattern = r'\d{4}-\d{8}'
        location_pattern = r'([A-Z0-9_,\.;#\'<>&\(\) /-]*) ([\w /]*)'
    # Extract text from each page
        for index,page in enumerate(reader.pages):
            text = page.extract_text()
            edge = False
            if text:  # Ensure there's text to process
                lines = text.split('\n')
                if(index==0):
                    lines = lines[1:]
                for index,line in enumerate(lines):
                    if(edge):
                        edge=False
                        continue
                    if line.startswith("Daily"):
                        continue
                    if "NORMAN POLICE DEPARTMENT" in line:
                        line = line.replace("NORMAN POLICE DEPARTMENT","")
                    match = re.search(pattern,line)
                    incident_number = ""
                    if(match):
                        incident_number = match.group()
                    line = line.split(" ")
                    if(len(line) ==2):
                        continue
                    if(index<(len(lines)-2)):
                        nextline = lines[index+1].split(" ")
                        if(len(nextline)<7 and  len(nextline)>2):
                            print(lines[index+1])
                            line = line+nextline
                            edge =True
                            
                    date_time = " ".join(line[0:2])
                    combi = " ".join(line[3:len(line)-1])
                    incident_ori = line[len(line)-1]
                    match = re.search(location_pattern,combi)
                    address =""
                    incident = ""
                    if match:
                        address = match.group(1)
                        incident = match.group(2)
                    # regex code to identify location and nature
                    data.append([date_time,incident_number,address,incident,incident_ori])# Store each line for CSV

    # Create a DataFrame and save as CSV
    df = pd.DataFrame(data)
    csv_file_path = './resources/output.csv'
    df.to_csv(csv_file_path, index=False, header =False)
    return df

def populatedb(db,incidents):
    incidents.to_sql('incidents', db, if_exists='replace', index=False)


def status(db):
    cur = db.cursor()
    # Execute the SELECT statement to retrieve all rows from the 'incidents' table
    cur.execute("SELECT * FROM incidents")
    rows = cur.fetchall()
    db.close()
    for row in rows:
        print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)

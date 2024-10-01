import argparse
import urllib.request
import pypdf
import re
import sqlite3
import pandas as pd
import os

def main(url):

    stats,pdf = fetch_incidents(url)
    if stats == 200:
        incidents = extract_incidents(pdf)
        db = create_db()
        populate_db(db, incidents)
        status(db)
    else:
        print("Unable to fetch data")
def fetch_incidents(url):
    
    response = urllib.request.urlopen(url)
    with open("./resources/data.pdf", "wb") as file:
        file.write(response.read())
    return response.getcode(),"./resources/data.pdf"

def create_db():

    db_path = "./resources/normanpd.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            incident_nature TEXT,
                incident_ori TEXT
        )
    """)
    con.commit()
    return con

def extract_incidents(pdf_path):

    data = []

    
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        incident_pattern = r'\d{4}-\d{8}'
        location_pattern = r'([A-Z0-9_,\.;#\'<>&\(\) /-]*) ([\w /]*)'    
        for index, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue       
            lines = text.split('\n')[1:] if index == 0 else text.split('\n')
            data.extend(parse_lines(lines, incident_pattern, location_pattern))
        return pd.DataFrame(data, columns=["incident_time", "incident_number", "incident_location", "incident_nature", "incident_ori"])

    
def parse_lines(lines, incident_pattern, location_pattern):
    
    data = []
    skip_next = False   
    for index, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue       
        if skip_text(line):
            continue       
        incident_number = ""
        match = re.search(incident_pattern, line)
        if match:
            match.group()
            
        list_words = process_multiline(lines, line, index)      
        date_time = " ".join(list_words[0:2])
        combined_info = " ".join(list_words[3:-1])
        incident_ori = list_words[-1]       
        match = re.search(location_pattern, combined_info)
        if match:
            address = match.group(1)
            incident_nature = match.group(2)
            data.append([date_time, incident_number, address, incident_nature, incident_ori])   
    return data

def skip_text(line):

    return line.startswith("Daily") or "NORMAN POLICE DEPARTMENT" in line


def process_multiline(lines, line, index):

    list_words = line.split(" ")
    
    if len(list_words) == 2:
        return list_words  # Malformed line, skip further processing
    
    if index < len(lines) - 2:
        next_line = lines[index + 1].split(" ")
        if len(next_line) < 7 and len(next_line) > 2:
            list_words += next_line  # Merge the next line into the current one
    
    return list_words

def populate_db(db, incidents):
 
    incidents.to_sql('incidents', db, if_exists='replace', index=False)

def status(db):
 
    cur = db.cursor()
    cur.execute("SELECT incident_nature, COUNT(*) FROM incidents GROUP BY incident_nature ORDER BY incident_nature ASC")
    rows = cur.fetchall()
    db.close()
    
    for row in rows:
        print(f"{row[0]} | {row[1]}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    args = parser.parse_args()
    main(args.incidents)

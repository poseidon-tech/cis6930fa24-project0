import argparse
import urllib.request
import pypdf
import re
import sqlite3
import pandas as pd
import os

#Global Variables
MODE_EXTRACTION = "layout"
MODE_LAYOUT = False

def main(url):
    stats, pdf = fetch_incidents(url)
    if stats == 200:
        incidents = extract_incidents(pdf)
        db = create_db()
        populate_db(db, incidents)
        status(db)
    else:
        pass
        # print("Unable to fetch data")


def fetch_incidents(url):
    response = urllib.request.urlopen(url)
    with open("./resources/data.pdf", "wb") as file:
        file.write(response.read())
    return response.getcode(), "./resources/data.pdf"


def create_db():
    db_path = "./resources/normanpd.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE incidents (
            time TEXT,
            incident_number TEXT,
            location TEXT,
            nature TEXT,
                incident_ORI TEXT
        )
    """)
    con.commit()
    return con


def extract_incidents(pdf_filepath):
    rows = []
    pdf_reader = pypdf.PdfReader(pdf_filepath)
    for page in pdf_reader.pages:
        text = page.extract_text(layout_mode_space_vertically=MODE_LAYOUT, extraction_mode=MODE_EXTRACTION)
        #print(text)
        if check_page(page):
            rows.extend(text.split('\n'))
        else:
            pass
            #print("No Text Found")
    result_data= parse_lines(rows[3:])
    df = pd.DataFrame(result_data, columns=["Date / Time", "Incident Number", "Location", "Nature","Incident ORI"])
    return df


def parse_lines(rows):
    pattern = r"(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2})\s+(\S+)\s+(.+?)(?=\s{2,}\S+)\s{2,}(.+?)\s{2,}(\S+)"

    parsed_data = []
    for row in rows:
        matches = re.findall(pattern, row)
        if matches:
            parsed_data.append(matches[0])
        else:
            pass
            # print("No match found")
    return parsed_data


def check_page(page):
    if(page):
        return True
    return False


def populate_db(db, incidents):
    incidents.to_sql('incidents', db, if_exists='replace', index=False)


def status(db):
    cur = db.cursor()
    cur.execute("SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC")
    rows = cur.fetchall()
    db.close()
    for row in rows:
        print(f"{row[0]}|{row[1]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    args = parser.parse_args()
    main(args.incidents)
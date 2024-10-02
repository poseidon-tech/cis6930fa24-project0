import argparse
import urllib.request
import pypdf
import re
import sqlite3
import pandas as pd
import os


def main(url):
    stats, pdf = fetch_incidents(url)
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
    return response.getcode(), "./resources/data.pdf"


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
    reader = pypdf.PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        if text:
            data.extend(text.split('\n'))
        else:
            print("No Text Found")
    records= parse_lines(data)
    df = pd.DataFrame(records, columns=["incident_time", "incident_number", "incident_location", "incident_nature", "incident_ori"])
    return df

def parse_lines(data):
    new_record = []
    for i in range(3, len(data) - 1):
        split_strings = re.split(r'\s{2,}', data[i])
        if split_strings[0] == '':
            continue
        while len(split_strings) < 5:
            split_strings.append('')
        new_record.append(split_strings)
    return new_record


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
        print(f"{row[0]}|{row[1]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    args = parser.parse_args()
    main(args.incidents)
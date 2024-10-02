import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'project0')))
from main import fetch_incidents, extract_incidents, create_db, populate_db, status, skip_text
resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
db_path = os.path.join(resources_path, 'normanpd.db')
test_data_path = os.path.join(resources_path, 'test_data.pdf')


def test_fetch_incidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-03_daily_incident_summary.pdf"
    response = fetch_incidents(url)
    assert os.path.exists(resources_path+"/data.pdf")  
    assert response[0] == 200
    assert os.path.getsize(resources_path+"/data.pdf") > 0  

def test_extract_incidents():
    incidents = extract_incidents(test_data_path)
    assert isinstance(incidents, pd.DataFrame)  
    assert len(incidents) > 0  
    
def test_skip_text():
    
    assert skip_text("Daily  Incident Summary (Public)") == True
    assert skip_text("NORMAN POLICE DEPARTMENT") == True

def test_create_db():
    con = create_db()
    assert os.path.exists(db_path)  
    cur = con.cursor()
    cur.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='incidents'
    """)  
    result = cur.fetchone()
    assert result is not None  
    con.close()

def test_populate_db():
    incidents = extract_incidents(test_data_path)
    con = create_db()
    populate_db(con, incidents)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM incidents")
    result = cur.fetchone()
    assert result[0] > 0  
    con.close()
    

def test_status_output(capsys):
    incidents = extract_incidents(test_data_path)
    db_conn = create_db()
    populate_db(db_conn, incidents)
    status(db_conn)
    captured = capsys.readouterr()
    assert "Traffic Stop" in captured.out  
    assert "|" in captured.out  
    assert "47" in captured.out
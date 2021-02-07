import sqlite3
from pathlib import Path

import scripts

build_sql = """
CREATE TABLE contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name CHAR(45),
    first_name CHAR(30),
    company CHAR(128),
    email CHAR(64),
    home_phone VARCHAR(20),
    work_phone VARCHAR(20),
    notes TEXT
);
"""

read_sql = """
    SELECT *
    FROM contacts
"""

db = "contacts.db"


def check_db():
    if not Path(db).is_file():
        import csv

        test_data_file = "dataFeb-6-2021.csv"
        test_data = []
        build_db()
        with open(test_data_file, "r") as test_file:
            reader = csv.reader(test_file)
            test_data = [r for r in reader]
        load_test_data(test_data)


def get_cursor():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    return cur


def build_db():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(build_sql)
    conn.commit()


def read_db():
    check_db()
    contacts = []
    cur = get_cursor()
    cur.execute(read_sql)
    contacts = [c for c in cur]
    return contacts


def add_contact(last, first, company, email, home_phone, work_phone):
    sql = scripts.add_conctact_sql
    params = (last, first, company, email, home_phone, work_phone)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()


def load_test_data(test_data):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = scripts.add_conctact_sql
    for row in test_data:
        try:
            cur.execute(sql, row)
            conn.commit()
        except:
            conn.rollback()
    return True


if __name__ == "__main__":

    contacts = read_db()
    print(len(contacts))

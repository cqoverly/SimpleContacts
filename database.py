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
    sql = scripts.create_table_sql
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def read_db():
    check_db()
    contacts = []
    cur = get_cursor()
    cur.execute(read_sql)
    contacts = [c for c in cur]
    return contacts


def get_contact(contact_id:int) -> list:
    sql = scripts.get_contact_sql
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, (contact_id,))
    contact = [c for c in cur.fetchone()]
    return contact


def add_contact(last, first, company, email, home_phone, work_phone):
    sql = scripts.add_conctact_sql
    params = (last, first, company, email, home_phone, work_phone)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()


def update_contact(contact:list):

    sql = scripts.update_contact_sql
    # last_name = params.get('last', None)
    # first_name = params.get('first', None)
    # company = params.get('company', None)
    # email = params.get('email', None)
    # home_phone = params.get('home', None)
    # work_phone = params.get('work', None)
    # notes = params.get('notes', None)
    # contact_id = params.get('contact_id', None)

    sql_params = (
        contact[1],
        contact[2],
        contact[3],
        contact[4],
        contact[5],
        contact[6],
        contact[7],
        contact[0]
    )
    print(sql_params)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, sql_params)
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

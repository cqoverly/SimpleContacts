import sqlite3

import database as db
import scripts



# SETUP

db_file = 'test_database.db'
def build_test_database():
    import csv

    test_data_file = "test_data.csv"
    test_data = []
    # Build the test sqlite3 db
    sql = scripts.create_table_sql
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    with open(test_data_file, "r") as test_file:
        reader = csv.reader(test_file)
        test_data = [r for r in reader]
    load_test_data(test_data)

def load_test_data(test_data):
    conn = sqlite3.connect(db_file)

    cur = conn.cursor()
    sql = scripts.add_conctact_sql
    for row in test_data[:11]:
        try:
            cur.execute(sql, row)
            conn.commit()
        except:
            conn.rollback()
    return True

load_test_data('test_data.csv')

try:
    build_test_database()
except sqlite3.OperationalError as e:
    print(e)

# TESTS

def test_get_contact():
    contact = db.get_contact(4)
    assert type(contact) == list
    assert len(contact) == 8


def test_read_db():
    contacts = db.read_db()
    assert len(contacts) > 0
    assert len(contacts[0]) == 8


def test_update_contact():
    contact = db.get_contact(4)
    params = [p for p in contact]
    company = 'My New Company'
    params2 = params[:]
    params2[3] = company
    db.update_contact(params2)
    contact2 = db.get_contact(4)
    assert contact[3] != contact2[3]
    db.update_contact(params)


def test_add_contact():
    contacts_before_add = db.read_db()
    last_name = f'Jones{len(contacts_before_add)}'
    first_name = 'Sam'
    company = 'Shiny Added Company'
    email = 'newmail@addmyemail.com'
    home = '(206)555)1234'
    work = ''
    note = 'This is a note from a test of add_contact'
    db.add_contact(
            f'{last_name}',
            first_name,
            company,
            email,
            home,
            work,
            note
        )
    contacts_after_add = db.read_db()
    assert len(contacts_after_add) == len(contacts_before_add) + 1
    db.delete_contact(f'{last_name}, {first_name}')


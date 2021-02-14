import logging
import sqlite3
from pathlib import Path

import scripts

# logger = logging.getLogger('app_logger')
# logging.basicConfig(
#         level=logging.DEBUG,
#         format='%(process)d - %(levelname)s - %(message)s')

db = "contacts.db"


def check_db():
    if not Path(db).is_file():
        import csv

        test_data_file = "test_data.csv"
        test_data = []
        build_db()
        with open(test_data_file, "r") as test_file:
            reader = csv.reader(test_file)
            test_data = [r for r in reader]
        load_test_data(test_data)
        # logger.info("Test dabase created.")


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
    sql = scripts.get_all_contacts_sql
    check_db()
    contacts = []
    cur = get_cursor()
    cur.execute(sql)
    contacts = [c for c in cur]
    return contacts


def get_contact(contact_id: int) -> list:
    sql = scripts.get_contact_sql
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, (contact_id,))
    contact = [c for c in cur.fetchone()]
    return contact


def add_contact(last, first, company, email, home_phone, work_phone, notes):
    sql = scripts.add_conctact_sql
    params = (last, first, company, email, home_phone, work_phone, notes)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()


def update_contact(contact: list):

    sql = scripts.update_contact_sql

    sql_params = (
        contact[1],
        contact[2],
        contact[3],
        contact[4],
        contact[5],
        contact[6],
        contact[7],
        contact[0],
    )
    logging.info(sql_params)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, sql_params)
    conn.commit()


def delete_contact(name):
    name = name.split(sep=',')
    last = name[0].strip()
    first = name[1].strip()
    sql = """
        SELECT * 
        FROM contacts
        WHERE last_name = ?
        AND first_name = ?
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql, (last, first))
    id = cur.fetchone()[0]
    print(f'ID is {id}')
    cur.execute(scripts.delete_contact, (id,))
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
    contacts.pop(0)
    # logger.info(f"{len(contacts)} records in database.")

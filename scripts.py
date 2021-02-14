create_table_sql = """
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
get_all_contacts_sql = """
    SELECT *
    FROM contacts
"""

get_contact_sql = """
    SELECT *
    FROM contacts
    WHERE contact_id = ?
"""


add_conctact_sql = """
    INSERT INTO contacts (
            last_name,
            first_name,
            company,
            email,
            home_phone,
            work_phone,
            notes
        )
        VALUES (?,?,?,?,?,?,?);
    """


update_contact_sql = """
    UPDATE contacts 
    SET last_name = ?,
    first_name = ?,
    company = ?,
    email = ?,
    home_phone = ?,
    work_phone = ?,
    notes = ?
    WHERE contact_id = ?;
"""

delete_contact = """
    DELETE FROM contacts
    WHERE contact_id = ?
"""
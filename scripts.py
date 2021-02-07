add_conctact_sql = '''
    INSERT INTO contacts (
            last_name,
            first_name,
            company,
            email,
            home_phone,
            work_phone
        )
        VALUES (?,?,?,?,?,?);
    '''